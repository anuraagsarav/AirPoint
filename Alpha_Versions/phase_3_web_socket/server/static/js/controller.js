const socket = io();


console.log("Connecting to server...");


socket.on("connect", () => {

    console.log("Connected to WebSocket server.");
});


socket.on("server_response", (data) => {

    console.log("Server Response:", data);
});


const moveButton =
    document.getElementById("moveButton");


moveButton.addEventListener("click", () => {

    const eventData = {

        event: "move",

        dx: 10,

        dy: -5
    };


    socket.emit("mouse_event", eventData);
});