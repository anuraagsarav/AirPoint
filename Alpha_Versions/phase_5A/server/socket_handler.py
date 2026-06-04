from flask_socketio import emit

from phase_5A.server.event_handler import handle_event

from phase_5A.server.connection_manager import (
    client_connected,
    client_disconnected
)


def register_socket_events(socketio):


    @socketio.on("connect")
    def handle_connect():

        client_connected()


    @socketio.on("disconnect")
    def handle_disconnect():

        client_disconnected()


    @socketio.on("mouse_event")
    def handle_mouse_event(data):

        handle_event(data)

        emit("server_response", {
            "status": "received",
            "data": data
        })