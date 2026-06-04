const socket = io();


// =====================================
// DOM ELEMENTS
// =====================================

const touchpad =
    document.getElementById("touchpad");


const leftClickButton =
    document.getElementById("left-click");


const rightClickButton =
    document.getElementById("right-click");


// =====================================
// MOVEMENT STATE
// =====================================

let previousX = null;
let previousY = null;


// =====================================
// THROTTLING SETTINGS
// =====================================

// Last time a movement packet was sent
let lastMoveTime = 0;


// Minimum delay between movement packets
// 8ms ≈ 120 FPS
const MOVE_INTERVAL = 8;


// =====================================
// SOCKET CONNECTION
// =====================================

socket.on("connect", () => {

    console.log(
        "Connected to WebSocket server."
    );
});


// =====================================
// SERVER RESPONSE
// =====================================

socket.on("server_response", (data) => {

    console.log(
        "SERVER RESPONSE:",
        data
    );
});


// =====================================
// GENERIC EVENT SENDER
// =====================================

function sendMouseEvent(eventData) {

    // Verify socket connection
    if (!socket.connected) {

        console.log(
            "Socket not connected"
        );

        return;
    }


    console.log(
        "SENDING EVENT:",
        eventData
    );


    socket.emit(
        "mouse_event",
        eventData
    );
}


// =====================================
// TOUCH START
// =====================================

touchpad.addEventListener(

    "touchstart",

    (event) => {

        const touch = event.touches[0];

        previousX = touch.clientX;
        previousY = touch.clientY;
    },

    { passive: false }
);


// =====================================
// TOUCH MOVE
// =====================================

touchpad.addEventListener(

    "touchmove",

    (event) => {

        event.preventDefault();


        // =====================================
        // FRAME THROTTLING
        // =====================================

        const now = Date.now();


        // Skip event if interval too small
        if (now - lastMoveTime < MOVE_INTERVAL) {

            return;
        }


        // Update last sent time
        lastMoveTime = now;


        // =====================================
        // TOUCH POSITION
        // =====================================

        const touch = event.touches[0];

        const currentX = touch.clientX;
        const currentY = touch.clientY;


        // =====================================
        // MOVEMENT DELTA
        // =====================================

        const dx = currentX - previousX;
        const dy = currentY - previousY;


        // Update previous position
        previousX = currentX;
        previousY = currentY;


        // =====================================
        // SEND MOVEMENT EVENT
        // =====================================

        sendMouseEvent({

            event: "move",

            dx: dx,

            dy: dy
        });

    },

    { passive: false }
);


// =====================================
// TOUCH END
// =====================================

touchpad.addEventListener(

    "touchend",

    () => {

        previousX = null;
        previousY = null;
    },

    { passive: false }
);


// =====================================
// LEFT CLICK BUTTON
// =====================================

leftClickButton.addEventListener(

    "touchstart",

    (event) => {

        event.preventDefault();


        console.log(
            "LEFT BUTTON PRESSED"
        );


        sendMouseEvent({

            event: "left_click"
        });

    },

    { passive: false }
);


// =====================================
// RIGHT CLICK BUTTON
// =====================================

rightClickButton.addEventListener(

    "touchstart",

    (event) => {

        event.preventDefault();


        console.log(
            "RIGHT BUTTON PRESSED"
        );


        sendMouseEvent({

            event: "right_click"
        });

    },

    { passive: false }
);