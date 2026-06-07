// Initialize socket after ensuring the Socket.IO client is available.
let socket = null;

const sessionToken = new URLSearchParams(window.location.search).get('token');
const deviceId = getOrCreateDeviceId();
const deviceName = getDeviceName();

function getOrCreateDeviceId() {
    const storageKey = 'airpoint_device_id';
    let storedDeviceId = localStorage.getItem(storageKey);

    if (storedDeviceId) {
        return storedDeviceId;
    }

    storedDeviceId = (
        crypto && crypto.randomUUID
    ) ? crypto.randomUUID() : createFallbackUuid();

    localStorage.setItem(storageKey, storedDeviceId);

    return storedDeviceId;
}

function createFallbackUuid() {
    return 'device-' + Date.now() + '-' + Math.random().toString(16).slice(2);
}

function getDeviceName() {
    if (navigator.userAgentData && navigator.userAgentData.platform) {
        return navigator.userAgentData.platform;
    }

    return navigator.platform || 'Mobile Browser';
}

function getSecurityPayload() {
    return {
        token: sessionToken,
        device_id: deviceId,
        device_name: deviceName
    };
}

function withSecurityPayload(data) {
    return Object.assign(
        {},
        data || {},
        getSecurityPayload()
    );
}

function initSocket(timeoutMs = 5000) {
    const start = Date.now();

    function attempt() {
        if (typeof io !== 'undefined') {
            socket = io({
                auth: getSecurityPayload(),
                query: {
                    token: sessionToken,
                    device_id: deviceId
                }
            });
            bindSocketEvents();
            return;
        }

        if (Date.now() - start < timeoutMs) {
            setTimeout(attempt, 100);
            return;
        }

        console.error('Socket.IO client not available. Check that socket.io.min.js is loaded.');
        setConnectionStatus('disconnected');
    }

    attempt();
}

function bindSocketEvents() {
    // Existing socket event handlers will attach to `socket` below.

    socket.on('connect', () => {
        console.log('Connected to AirPoint');
        setConnectionStatus('connected');
        switchMode('normal');
        measureLatency();
        setInterval(measureLatency, 2000);
    });

    socket.on('disconnect', () => {
        console.log('Disconnected from AirPoint');
        setConnectionStatus('disconnected');
    });

    socket.on('connect_error', (error) => {
        console.error('AirPoint connection rejected:', error.message);
        setConnectionStatus('disconnected');
    });

    socket.io.on('reconnect_attempt', () => {
        setConnectionStatus('connecting');
    });

    socket.on('pong', (data) => {
        // Latency measured in measureLatency function
    });
}



// =========================================
// DOM ELEMENTS
// =========================================

const touchpad =
    document.getElementById(
        "touchpad"
    );

const normalModeButton =
    document.getElementById(
        "normal-mode-button"
    );

const presentationModeButton =
    document.getElementById(
        "presentation-mode-button"
    );

const normalModeView =
    document.getElementById(
        "normal-mode-view"
    );

const presentationModeView =
    document.getElementById(
        "presentation-mode-view"
    );

const startSlideshowButton =
    document.getElementById(
        "start-slideshow-button"
    );

const exitSlideshowButton =
    document.getElementById(
        "exit-slideshow-button"
    );

const presentationTouchpad =
    document.getElementById(
        "presentation-touchpad"
    );

const previousSlideButton =
    document.getElementById(
        "previous-slide-button"
    );

const nextSlideButton =
    document.getElementById(
        "next-slide-button"
    );

const statusIndicator =
    document.getElementById(
        "status-indicator"
    );

const statusText =
    document.getElementById(
        "status-text"
    );

const connectionStatus =
    document.getElementById(
        "connection-status"
    );

const networkStatsOverlay =
    document.getElementById(
        "network-stats-overlay"
    );

const networkLatencyValue =
    document.getElementById(
        "network-latency-value"
    );

const networkSpeedValue =
    document.getElementById(
        "network-speed-value"
    );

const airpointConfig = window.AIRPOINT_CONFIG || {
    showNetworkStats: false
};


// =========================================
// MODE STATE
// =========================================

let currentMode = "normal";


// =========================================
// NORMAL TOUCHPAD STATE
// =========================================

let previousX = null;
let previousY = null;

let touchStartX = 0;
let touchStartY = 0;

let gestureMode = null;

let gestureStartTime = 0;

let gestureMoved = false;

let clickLock = false;


// =========================================
// MOVEMENT BUFFER
// =========================================

let deltaX = 0;
let deltaY = 0;

let flushScheduled = false;

let lastMoveTime = 0;
let pendingFlushTimer = null;


// =========================================
// PRESENTATION STATE
// =========================================

let presentationPreviousX = null;
let presentationPreviousY = null;

let presentationTouchStartX = 0;
let presentationTouchStartY = 0;

let presentationGestureMode = null;

let presentationGestureStartTime = 0;

let presentationGestureMoved = false;


// =========================================
// NETWORK MONITORING
// =========================================

let networkLatency = 0;
let packetsSent = 0;
let packetsAcked = 0;
let currentNetworkProfile = "high";

const NETWORK_LATENCY_THRESHOLDS = {
    high: 80,
    medium: 180
};

const NETWORK_SETTINGS = {
    high: {
        moveInterval: 0,
        scrollInterval: 16,
        sensitivityScale: 1.1
    },
    medium: {
        moveInterval: 16,
        scrollInterval: 24,
        sensitivityScale: 1.0
    },
    low: {
        moveInterval: 32,
        scrollInterval: 40,
        sensitivityScale: 0.85
    }
};

let currentMoveInterval = NETWORK_SETTINGS.high.moveInterval;
let currentScrollInterval = NETWORK_SETTINGS.high.scrollInterval;
let currentSensitivityScale = NETWORK_SETTINGS.high.sensitivityScale;

let scrollDelta = 0;
let scrollFlushScheduled = false;
let lastScrollTime = 0;

let presentationScrollDelta = 0;
let presentationScrollFlushScheduled = false;
let lastPresentationScrollTime = 0;


function updateNetworkQuality() {
    const previousProfile = currentNetworkProfile;

    if (networkLatency < NETWORK_LATENCY_THRESHOLDS.high) {
        currentNetworkProfile = "high";
    } else if (networkLatency < NETWORK_LATENCY_THRESHOLDS.medium) {
        currentNetworkProfile = "medium";
    } else {
        currentNetworkProfile = "low";
    }

    const settings = NETWORK_SETTINGS[currentNetworkProfile];
    currentMoveInterval = settings.moveInterval;
    currentScrollInterval = settings.scrollInterval;
    currentSensitivityScale = settings.sensitivityScale;

    if (previousProfile !== currentNetworkProfile) {
        console.debug(
            `Network profile changed to ${currentNetworkProfile}`,
            `latency=${networkLatency}ms`,
            `moveInterval=${currentMoveInterval}`
        );
    }

    updateNetworkStatsDisplay();
}


function updateNetworkStatsDisplay() {
    if (!airpointConfig.showNetworkStats || !networkStatsOverlay) {
        return;
    }

    networkStatsOverlay.classList.remove('hidden');
    networkLatencyValue.innerText = `${networkLatency} ms`;
    networkSpeedValue.innerText = currentNetworkProfile;
}

function hideNetworkStatsDisplay() {
    if (networkStatsOverlay) {
        networkStatsOverlay.classList.add('hidden');
    }
}

function measureLatency() {
    const timestamp = Date.now();

    emitSafe("ping", { ts: timestamp }, (response) => {
        networkLatency = Date.now() - timestamp;
        updateNetworkQuality();
    });
}


// ==========================
// Socket helpers
// ==========================
function isSocketReady() {
    return socket && socket.connected;
}

function emitSafe(event, data, ack) {
    if (!isSocketReady()) {
        console.warn('emit skipped, socket not ready:', event);
        return;
    }

    if (typeof ack === 'function') {
        socket.emit(event, withSecurityPayload(data), ack);
    } else {
        socket.emit(event, withSecurityPayload(data));
    }
}

function volatileEmitSafe(event, data) {
    if (!isSocketReady()) {
        return;
    }

    if (socket.volatile) {
        socket.volatile.emit(event, withSecurityPayload(data));
    } else {
        socket.emit(event, withSecurityPayload(data));
    }
}


// =========================================
// CONNECTION STATUS UI
// =========================================

function setConnectionStatus(status) {

    // =====================================
    // CONNECTED
    // =====================================

    if (status === "connected") {

        statusIndicator.style.background =
            "#57d38c";

        statusIndicator.style.boxShadow =
            "0 0 10px #57d38c";

        statusText.innerText =
            "Connected";
    }


    // =====================================
    // DISCONNECTED
    // =====================================

    else if (status === "disconnected") {

        statusIndicator.style.background =
            "#ff4d4d";

        statusIndicator.style.boxShadow =
            "0 0 10px #ff4d4d";

        statusText.innerText =
            "Disconnected";
    }


    // =====================================
    // CONNECTING
    // =====================================

    else {

        statusIndicator.style.background =
            "#ffaa33";

        statusIndicator.style.boxShadow =
            "0 0 10px #ffaa33";

        statusText.innerText =
            "Connecting...";
    }

}

// =========================================
// SOCKET EVENTS
// =========================================

// If the Socket.IO client script is still loading, initSocket will attach handlers.
initSocket();


// =========================================
// MODE SWITCHING
// =========================================

function switchMode(mode) {

    currentMode = mode;


    // =====================================
    // REMOVE ACTIVE STATE
    // =====================================

    normalModeButton.classList.remove(
        "active-nav"
    );

    presentationModeButton.classList.remove(
        "active-nav"
    );


    // =====================================
    // UPDATE SERVER MODE
    // =====================================

    emitSafe(
        "set_mode",
        {
            mode: mode
        }
    );


    // =====================================
    // NORMAL MODE
    // =====================================

    if (mode === "normal") {

        normalModeView.style.display =
            "flex";

        presentationModeView.style.display =
            "none";


        normalModeButton.classList.add(
            "active-nav"
        );

    }


    // =====================================
    // PRESENTATION MODE
    // =====================================

    else {

        normalModeView.style.display =
            "none";

        presentationModeView.style.display =
            "flex";


        presentationModeButton.classList.add(
            "active-nav"
        );

    }

}

// =========================================
// MODE BUTTONS
// =========================================

normalModeButton.addEventListener(

    "click",

    () => {

        switchMode("normal");
    }

);


presentationModeButton.addEventListener(

    "click",

    () => {

        switchMode("presentation");
    }

);


previousSlideButton.addEventListener(

    "click",

    () => {

        emitSafe(
            "previous_slide"
        );

    }

);


nextSlideButton.addEventListener(

    "click",

    () => {

        emitSafe(
            "next_slide"
        );

    }

);


// =========================================
// CLICK STABILIZATION
// =========================================

function lockMovementTemporarily() {

    clickLock = true;


    setTimeout(

        () => {

            clickLock = false;

        },

        30

    );

}


// =========================================
// SEND MOVEMENT
// =========================================

function sendMovement(dx, dy) {
    if (!isSocketReady()) {
        return;
    }

    const scaledDx = dx * currentSensitivityScale;
    const scaledDy = dy * currentSensitivityScale;

    volatileEmitSafe(
        "mouse_move",
        {
            dx: scaledDx,
            dy: scaledDy
        }
    );

}


// =========================================
// SEND SCROLL
// =========================================

function sendScroll(dy) {
    if (!isSocketReady()) {
        return;
    }

    emitSafe(
        "mouse_scroll",
        {
            dy: dy
        }
    );

}


// =========================================
// SEND PRESENTATION CURSOR SCROLL
// =========================================

function sendPresentationCursorScroll(dy) {
    if (!isSocketReady()) {
        return;
    }

    emitSafe(
        "presentation_cursor_scroll",
        {
            dy: dy
        }
    );

}


// =========================================
// FLUSH SCROLL
// =========================================

function flushScroll() {

    if (scrollDelta === 0) {
        scrollFlushScheduled = false;
        return;
    }

    sendScroll(scrollDelta);
    scrollDelta = 0;
    scrollFlushScheduled = false;
    lastScrollTime = Date.now();
}


// =========================================
// FLUSH PRESENTATION SCROLL
// =========================================

function flushPresentationScroll() {

    if (presentationScrollDelta === 0) {
        presentationScrollFlushScheduled = false;
        return;
    }

    sendPresentationCursorScroll(presentationScrollDelta);
    presentationScrollDelta = 0;
    presentationScrollFlushScheduled = false;
    lastPresentationScrollTime = Date.now();
}


// =========================================
// SCHEDULE SCROLL FLUSH
// =========================================

function scheduleScrollFlush(dy) {

    scrollDelta += dy;

    if (scrollFlushScheduled) {
        return;
    }

    scrollFlushScheduled = true;

    const now = Date.now();
    const elapsed = now - lastScrollTime;
    const waitTime = Math.max(0, currentScrollInterval - elapsed);

    if (waitTime === 0) {
        flushScroll();
    } else {
        setTimeout(flushScroll, waitTime);
    }
}


// =========================================
// SCHEDULE PRESENTATION SCROLL FLUSH
// =========================================

function schedulePresentationScrollFlush(dy) {

    presentationScrollDelta += dy;

    if (presentationScrollFlushScheduled) {
        return;
    }

    presentationScrollFlushScheduled = true;

    const now = Date.now();
    const elapsed = now - lastPresentationScrollTime;
    const waitTime = Math.max(0, currentScrollInterval - elapsed);

    if (waitTime === 0) {
        flushPresentationScroll();
    } else {
        setTimeout(flushPresentationScroll, waitTime);
    }
}


// =========================================
// FLUSH MOVEMENT
// =========================================

function flushMovement() {

    if (
        deltaX === 0 &&
        deltaY === 0
    ) {

        flushScheduled = false;
        pendingFlushTimer = null;

        return;
    }


    sendMovement(
        deltaX,
        deltaY
    );


    deltaX = 0;
    deltaY = 0;

    flushScheduled = false;
    pendingFlushTimer = null;

    lastMoveTime = Date.now();
}


// =========================================
// SCHEDULE FLUSH
// =========================================

function scheduleFlush() {

    if (pendingFlushTimer !== null) {
        return;
    }

    if (currentMoveInterval === 0 && typeof requestAnimationFrame === 'function') {
        pendingFlushTimer = requestAnimationFrame(flushMovement);
    } else {
        pendingFlushTimer = setTimeout(
            flushMovement,
            currentMoveInterval
        );
    }
}


// =========================================
// NORMAL TOUCHPAD START
// =========================================

touchpad.addEventListener(

    "touchstart",

    (event) => {

        if (currentMode !== "normal") {
            return;
        }


        gestureStartTime = Date.now();

        gestureMoved = false;


        // =====================================
        // SINGLE FINGER
        // =====================================

        if (event.touches.length === 1) {

            gestureMode = "move";


            const touch =
                event.touches[0];


            previousX =
                touch.clientX;

            previousY =
                touch.clientY;


            touchStartX =
                touch.clientX;

            touchStartY =
                touch.clientY;
        }


        // =====================================
        // TWO FINGER
        // =====================================

        else if (event.touches.length === 2) {

            gestureMode = "scroll";


            const touch1 =
                event.touches[0];

            const touch2 =
                event.touches[1];


            previousY = (

                touch1.clientY +

                touch2.clientY

            ) / 2;
        }

    },

    { passive: false }

);


// =========================================
// NORMAL TOUCHPAD MOVE
// =========================================

touchpad.addEventListener(

    "touchmove",

    (event) => {

        if (currentMode !== "normal") {
            return;
        }


        event.preventDefault();


        if (clickLock) {
            return;
        }


        // =====================================
        // TWO FINGER SCROLL
        // =====================================

        if (

            gestureMode === "scroll" &&

            event.touches.length === 2

        ) {

            const touch1 =
                event.touches[0];

            const touch2 =
                event.touches[1];


            const avgY = (

                touch1.clientY +

                touch2.clientY

            ) / 2;


            if (previousY !== null) {

                const dy =
                    avgY - previousY;


                if (Math.abs(dy) > 4) {

                    gestureMoved = true;
                }


                scheduleScrollFlush(dy);
            }


            previousY = avgY;

            return;
        }


        // =====================================
        // NORMAL MOVEMENT
        // =====================================

        if (
            gestureMode !== "move"
        ) {
            return;
        }


        const touch =
            event.touches[0];


        const currentX =
            touch.clientX;

        const currentY =
            touch.clientY;


        if (

            previousX === null ||

            previousY === null

        ) {

            previousX = currentX;
            previousY = currentY;

            return;
        }


        const dx =
            currentX - previousX;

        const dy =
            currentY - previousY;


        // =====================================
        // MOVEMENT THRESHOLD
        // =====================================

        if (

            Math.abs(
                currentX - touchStartX
            ) > 12 ||

            Math.abs(
                currentY - touchStartY
            ) > 12

        ) {

            gestureMoved = true;
        }


        previousX = currentX;
        previousY = currentY;


        deltaX += dx;
        deltaY += dy;


        scheduleFlush();

    },

    { passive: false }

);


// =========================================
// NORMAL TOUCHPAD END
// =========================================

touchpad.addEventListener(

    "touchend",

    () => {

        if (currentMode !== "normal") {
            return;
        }


        const duration =
            Date.now() - gestureStartTime;


        // =====================================
        // LEFT CLICK
        // =====================================

        if (

            gestureMode === "move" &&

            !gestureMoved &&

            duration < 300

        ) {

            lockMovementTemporarily();

            console.log('Attempting left_click (duration:', duration, 'gestureMoved:', gestureMoved, ')');

            emitSafe(
                "left_click"
            );
        }


        // =====================================
        // RIGHT CLICK
        // =====================================

        else if (

            gestureMode === "scroll" &&

            !gestureMoved &&

            duration < 350

        ) {

            lockMovementTemporarily();

            console.log('Attempting right_click (duration:', duration, 'gestureMoved:', gestureMoved, ')');

            emitSafe(
                "right_click"
            );
        }


        previousX = null;
        previousY = null;

        gestureMode = null;

    },

    { passive: false }

);


// =========================================
// START SLIDESHOW
// =========================================

startSlideshowButton.addEventListener(

    "click",

    () => {

        emitSafe(
            "start_presentation"
        );

    }

);


// =========================================
// EXIT SLIDESHOW
// =========================================

exitSlideshowButton.addEventListener(

    "click",

    () => {

        emitSafe(
            "exit_presentation"
        );

    }

);


// =========================================
// PRESENTATION TOUCH START
// =========================================

presentationTouchpad.addEventListener(

    "touchstart",

    (event) => {

        if (currentMode !== "presentation") {
            return;
        }


        event.preventDefault();

        presentationGestureStartTime =
            Date.now();

        presentationGestureMoved =
            false;

        if (event.touches.length === 1) {

            presentationGestureMode =
                "move";

            const touch =
                event.touches[0];


            presentationPreviousX =
                touch.clientX;

            presentationPreviousY =
                touch.clientY;


            presentationTouchStartX =
                touch.clientX;

            presentationTouchStartY =
                touch.clientY;
        }

        else if (event.touches.length === 2) {

            presentationGestureMode =
                "scroll";

            const touch1 =
                event.touches[0];

            const touch2 =
                event.touches[1];


            presentationPreviousY = (

                touch1.clientY +

                touch2.clientY

            ) / 2;
        }

    },

    { passive: false }

);


// =========================================
// PRESENTATION TOUCH MOVE
// =========================================

presentationTouchpad.addEventListener(

    "touchmove",

    (event) => {

        if (currentMode !== "presentation") {
            return;
        }


        event.preventDefault();


        if (clickLock) {
            return;
        }


        // =====================================
        // TWO FINGER SCROLL
        // =====================================

        if (

            presentationGestureMode ===
            "scroll" &&

            event.touches.length === 2

        ) {

            const touch1 =
                event.touches[0];

            const touch2 =
                event.touches[1];


            const avgY = (

                touch1.clientY +

                touch2.clientY

            ) / 2;


            if (presentationPreviousY !== null) {

                const dy =
                    avgY - presentationPreviousY;


                if (Math.abs(dy) > 4) {

                    presentationGestureMoved =
                        true;
                }


                schedulePresentationScrollFlush(dy);
            }


            presentationPreviousY =
                avgY;

            return;
        }


        if (
            presentationGestureMode !==
            "move"
        ) {
            return;
        }


        const touch =
            event.touches[0];


        const currentX =
            touch.clientX;

        const currentY =
            touch.clientY;


        if (

            presentationPreviousX === null ||

            presentationPreviousY === null

        ) {

            presentationPreviousX =
                currentX;

            presentationPreviousY =
                currentY;

            return;
        }


        const dx =
            currentX -
            presentationPreviousX;

        const dy =
            currentY -
            presentationPreviousY;


        if (

            Math.abs(
                currentX - presentationTouchStartX
            ) > 12 ||

            Math.abs(
                currentY - presentationTouchStartY
            ) > 12

        ) {

            presentationGestureMoved =
                true;
        }


        presentationPreviousX =
            currentX;

        presentationPreviousY =
            currentY;


        sendMovement(
            dx * 1.3,
            dy * 1.3
        );

    },

    { passive: false }

);


// =========================================
// PRESENTATION TOUCH END
// =========================================

presentationTouchpad.addEventListener(

    "touchend",

    (event) => {

        if (currentMode !== "presentation") {
            return;
        }


        const duration =
            Date.now() - presentationGestureStartTime;


        if (

            presentationGestureMode ===
            "move" &&

            !presentationGestureMoved &&

            duration < 300

        ) {

            lockMovementTemporarily();

            emitSafe(
                "presentation_cursor_left_click"
            );
        }


        else if (

            presentationGestureMode ===
            "scroll" &&

            !presentationGestureMoved &&

            duration < 350

        ) {

            lockMovementTemporarily();

            emitSafe(
                "presentation_cursor_right_click"
            );
        }


        presentationPreviousX =
            null;

        presentationPreviousY =
            null;

        presentationGestureMode =
            null;

    },

    { passive: false }

);


