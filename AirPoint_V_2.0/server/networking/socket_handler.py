from flask import request
from flask_socketio import disconnect

from server.input_engine.movement_processor import (
    process_movement
)

from server.input_engine.gesture_processor import (
    process_left_click,
    process_right_click
)

from server.input_engine.scroll_processor import (
    process_scroll
)

from server.input_engine.smoothing_engine import (
    clear_device_state as clear_smoothing_state
)

from server.controllers.mouse_controller import (
    clear_device_state as clear_mouse_state
)

from server.controllers.presentation_controller import (

    go_to_next_slide,

    go_to_previous_slide,

    start_presentation,

    exit_presentation
)

from server.modes.mode_manager import (
    set_mode,
    get_mode
)

from server.session.active_session import (
    register_device,
    remove_device
)


# ==========================================
# REGISTER SOCKET EVENTS
# ==========================================

def register_socket_events(socketio):


    @socketio.on("connect")
    def handle_connect(auth=None):

        device_ip = request.remote_addr

        old_sid = register_device(
            request.sid,
            device_ip
        )

        if old_sid and old_sid != request.sid:
            disconnect(old_sid)

        print("\n=================================")
        print("AIRPOINT DEVICE CONNECTED")
        print(f"IP ADDRESS : {device_ip}")
        print(f"SESSION ID : {request.sid}")
        print("=================================\n")


    @socketio.on("disconnect")
    def handle_disconnect():

        device_id = request.sid
        remove_device(device_id)

        clear_smoothing_state(device_id)
        clear_mouse_state(device_id)

        print("\n=================================")
        print("AIRPOINT DEVICE DISCONNECTED")
        print(f"SESSION ID : {device_id}")
        print("=================================\n")


    # ======================================
    # LATENCY MONITORING
    # ======================================

    @socketio.on("ping")
    def handle_ping(data):
        socketio.emit("pong", data, to=request.sid)


    # ======================================
    # MODE CHANGE
    # ======================================

    @socketio.on("set_mode")
    def handle_set_mode(data):

        mode = data.get("mode")

        set_mode(mode)


    # ======================================
    # NORMAL MODE EVENTS
    # ======================================

    @socketio.on("mouse_move")
    def handle_mouse_move(data):

        process_movement(data, request.sid)


    @socketio.on("left_click")
    def handle_left_click(*args, **kwargs):

        if get_mode() != "normal":
            return

        process_left_click()


    @socketio.on("right_click")
    def handle_right_click(*args, **kwargs):

        if get_mode() != "normal":
            return

        process_right_click()


    @socketio.on("mouse_scroll")
    def handle_scroll(data):

        if get_mode() != "normal":
            return

        process_scroll(data)


    # ======================================
    # PRESENTATION EVENTS
    # ======================================

    @socketio.on("next_slide")
    def handle_next_slide(*args, **kwargs):

        go_to_next_slide()


    @socketio.on("previous_slide")
    def handle_previous_slide(*args, **kwargs):

        go_to_previous_slide()


    @socketio.on("start_presentation")
    def handle_start_presentation(*args, **kwargs):

        start_presentation()


    @socketio.on("exit_presentation")
    def handle_exit_presentation(*args, **kwargs):

        exit_presentation()