const socket = io();


const touchpad =
    document.getElementById("touchpad");


let previousX = null;
let previousY = null;


socket.on("connect", () => {

    console.log("Connected to WebSocket server.");
});


touchpad.addEventListener("touchstart", (event) => {

    const touch = event.touches[0];

    previousX = touch.clientX;
    previousY = touch.clientY;

});


touchpad.addEventListener("touchmove", (event) => {

    event.preventDefault();

    const touch = event.touches[0];

    const currentX = touch.clientX;
    const currentY = touch.clientY;


    const dx = currentX - previousX;
    const dy = currentY - previousY;


    previousX = currentX;
    previousY = currentY;


    const movementData = {

        event: "move",

        dx: dx,

        dy: dy
    };


    socket.emit("mouse_event", movementData);

});


touchpad.addEventListener("touchend", () => {

    previousX = null;
    previousY = null;
});