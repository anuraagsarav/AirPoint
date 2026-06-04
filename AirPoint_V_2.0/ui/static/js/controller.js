// Initialize socket after ensuring the Socket.IO client is available.
let socket = null;

function initSocket(timeoutMs = 5000) {
    const start = Date.now();

    function attempt() {
        if (typeof io !== 'undefined') {
            socket = io();
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

const presentationNavigationButton =
    document.getElementById(
        "presentation-navigation-button"
    );

const presentationCursorButton =
    document.getElementById(
        "presentation-cursor-button"
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


// =========================================
// MODE STATE
// =========================================

let currentMode = "normal";

let presentationSubMode =
    "navigation";


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

const MOVE_INTERVAL = 4;

let lastMoveTime = 0;
let pendingFlushTimer = null;


// =========================================
// PRESENTATION STATE
// =========================================

let presentationPreviousX = null;
let presentationPreviousY = null;

let swipeStartX = 0;
let swipeStartY = 0;

let swipeStartTime = 0;


// =========================================
// NETWORK MONITORING
// =========================================

let networkLatency = 0;
let packetsSent = 0;
let packetsAcked = 0;
let networkQuality = "good";

const LATENCY_THRESHOLDS = {
    good: 50,
    fair: 150,
    poor: 300
};

const MOVE_INTERVALS = {
    good: 4,
    fair: 8,
    poor: 12
};

let currentMoveInterval = MOVE_INTERVALS.good;

let scrollDelta = 0;
let scrollFlushScheduled = false;
let lastScrollTime = 0;


function updateNetworkQuality() {
    if (networkLatency < LATENCY_THRESHOLDS.good) {
        networkQuality = "good";
    } else if (networkLatency < LATENCY_THRESHOLDS.fair) {
        networkQuality = "fair";
    } else {
        networkQuality = "poor";
    }

    currentMoveInterval = MOVE_INTERVALS[networkQuality];
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
        socket.emit(event, data, ack);
    } else {
        socket.emit(event, data);
    }
}

function volatileEmitSafe(event, data) {
    if (!isSocketReady()) {
        return;
    }

    if (socket.volatile) {
        socket.volatile.emit(event, data);
    } else {
        socket.emit(event, data);
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
// PRESENTATION SUB MODE
// =========================================

function setPresentationSubMode(mode) {

    presentationSubMode = mode;


    if (mode === "navigation") {

        presentationNavigationButton.style.background =
            "#4d7cff";

        presentationCursorButton.style.background =
            "#202733";
    }

    else {

        presentationNavigationButton.style.background =
            "#202733";

        presentationCursorButton.style.background =
            "#4d7cff";
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


presentationNavigationButton.addEventListener(

    "click",

    () => {

        setPresentationSubMode(
            "navigation"
        );

    }

);


presentationCursorButton.addEventListener(

    "click",

    () => {

        setPresentationSubMode(
            "cursor"
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

    volatileEmitSafe(
        "mouse_move",
        {
            dx: dx,
            dy: dy
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
    const waitTime = Math.max(0, currentMoveInterval * 1.5 - elapsed);

    if (waitTime === 0) {
        flushScroll();
    } else {
        setTimeout(flushScroll, waitTime);
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

    const now = Date.now();
    const elapsed = now - lastMoveTime;
    const waitTime = Math.max(0, currentMoveInterval - elapsed);

    if (waitTime === 0) {
        flushMovement();
    } else {
        pendingFlushTimer = setTimeout(
            flushMovement,
            waitTime
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


        // =====================================
        // CURSOR MODE
        // =====================================

        if (
            presentationSubMode ===
            "cursor"
        ) {

            const touch =
                event.touches[0];


            presentationPreviousX =
                touch.clientX;

            presentationPreviousY =
                touch.clientY;

            return;
        }


        // =====================================
        // NAVIGATION MODE
        // =====================================

        const touch =
            event.touches[0];


        swipeStartX =
            touch.clientX;

        swipeStartY =
            touch.clientY;

        swipeStartTime =
            Date.now();

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


        // =====================================
        // CURSOR MODE
        // =====================================

        if (
            presentationSubMode ===
            "cursor"
        ) {

            event.preventDefault();


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


            presentationPreviousX =
                currentX;

            presentationPreviousY =
                currentY;


            sendMovement(
                dx * 1.3,
                dy * 1.3
            );

        }

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


        // =====================================
        // CURSOR MODE
        // =====================================

        if (
            presentationSubMode ===
            "cursor"
        ) {

            presentationPreviousX =
                null;

            presentationPreviousY =
                null;

            return;
        }


        // =====================================
        // NAVIGATION MODE
        // =====================================

        const duration =
            Date.now() - swipeStartTime;


        if (duration > 500) {
            return;
        }


        const touch =
            event.changedTouches[0];


        const dx =
            touch.clientX - swipeStartX;

        const dy =
            touch.clientY - swipeStartY;


        // =====================================
        // SWIPE DETECTION
        // =====================================

        if (

            Math.abs(dx) > 120 &&

            Math.abs(dy) < 80

        ) {

            // =================================
            // SWIPE LEFT
            // =================================

                if (dx < 0) {

                emitSafe(
                    "next_slide"
                );
            }


            // =================================
            // SWIPE RIGHT
            // =================================

                else {

                emitSafe(
                    "previous_slide"
                );
            }

        }

    },

    { passive: false }

);


// =========================================
// DEFAULT PRESENTATION MODE
// =========================================

setPresentationSubMode(
    "navigation"
);