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
from server.security.access_control import (
    register_authorized_connection,
    remove_authorized_connection,
    validate_socket_event
)
from server.security.approval_dialog import (
    request_device_approval
)
from server.security.security_logger import (
    log_info,
    log_warning
)
from server.security.session_token import (
    is_valid_session_token
)
from server.security.trusted_devices import (
    is_trusted_device,
    update_last_seen
)


# ==========================================
# REGISTER SOCKET EVENTS
# ==========================================

def register_socket_events(socketio):


    @socketio.on("connect")
    def handle_connect(auth=None):

        device_ip = request.remote_addr
        auth = auth or {}
        token = auth.get("token") or request.args.get("token")
        device_id = auth.get("device_id") or request.args.get("device_id")
        device_name = auth.get("device_name") or "Unknown Device"

        if not is_valid_session_token(token):
            log_warning(
                "Invalid session token",
                ip_address=device_ip,
                sid=getattr(request, "sid")
            )
            return False

        if not device_id:
            log_warning(
                "Unknown device rejected",
                ip_address=device_ip,
                reason="missing_device_id"
            )
            return False

        if is_trusted_device(device_id):
            update_last_seen(device_id, device_ip)
        else:
            approved = request_device_approval(
                device_id,
                device_name,
                device_ip
            )

            if not approved:
                return False

        old_sid = register_device(
            getattr(request, "sid"),
            device_ip
        )

        register_authorized_connection(
            getattr(request, "sid"),
            device_id
        )

        if old_sid and old_sid != getattr(request, "sid"):
            disconnect(old_sid)

        log_info(
            "Trusted device connected",
            device_id=device_id,
            device_name=device_name,
            ip_address=device_ip
        )

        print("\n=================================")
        print("AIRPOINT DEVICE CONNECTED")
        print(f"DEVICE NAME: {device_name}")
        print(f"IP ADDRESS : {device_ip}")
        print(f"SESSION ID : {getattr(request, 'sid')}")
        print("=================================\n")


    @socketio.on("disconnect")
    def handle_disconnect():

        device_id = getattr(request, "sid")
        remove_device(device_id)
        remove_authorized_connection(device_id)

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
        if not validate_socket_event(getattr(request, "sid"), data):
            disconnect()
            return

        socketio.emit("pong", data, to=getattr(request, "sid"))


    # ======================================
    # MODE CHANGE
    # ======================================

    @socketio.on("set_mode")
    def handle_set_mode(data):
        if not validate_socket_event(getattr(request, "sid"), data):
            disconnect()
            return

        mode = data.get("mode")

        set_mode(mode)


    # ======================================
    # NORMAL MODE EVENTS
    # ======================================

    @socketio.on("mouse_move")
    def handle_mouse_move(data):
        if not validate_socket_event(getattr(request, "sid"), data):
            disconnect()
            return

        process_movement(data, getattr(request, "sid"))


    @socketio.on("left_click")
    def handle_left_click(data=None):
        if not validate_socket_event(getattr(request, "sid"), data):
            disconnect()
            return

        if get_mode() != "normal":
            return

        process_left_click()


    @socketio.on("right_click")
    def handle_right_click(data=None):
        if not validate_socket_event(getattr(request, "sid"), data):
            disconnect()
            return

        if get_mode() != "normal":
            return

        process_right_click()


    @socketio.on("mouse_scroll")
    def handle_scroll(data):
        if not validate_socket_event(getattr(request, "sid"), data):
            disconnect()
            return

        if get_mode() != "normal":
            return

        process_scroll(data)


    # ======================================
    # PRESENTATION EVENTS
    # ======================================

    @socketio.on("next_slide")
    def handle_next_slide(data=None):
        if not validate_socket_event(getattr(request, "sid"), data):
            disconnect()
            return

        go_to_next_slide()


    @socketio.on("previous_slide")
    def handle_previous_slide(data=None):
        if not validate_socket_event(getattr(request, "sid"), data):
            disconnect()
            return

        go_to_previous_slide()


    @socketio.on("presentation_cursor_left_click")
    def handle_presentation_cursor_left_click(data=None):
        if not validate_socket_event(getattr(request, "sid"), data):
            disconnect()
            return

        if get_mode() != "presentation":
            return

        process_left_click()


    @socketio.on("presentation_cursor_right_click")
    def handle_presentation_cursor_right_click(data=None):
        if not validate_socket_event(getattr(request, "sid"), data):
            disconnect()
            return

        if get_mode() != "presentation":
            return

        process_right_click()


    @socketio.on("presentation_cursor_scroll")
    def handle_presentation_cursor_scroll(data):
        if not validate_socket_event(getattr(request, "sid"), data):
            disconnect()
            return

        if get_mode() != "presentation":
            return

        process_scroll(data)


    @socketio.on("start_presentation")
    def handle_start_presentation(data=None):
        if not validate_socket_event(getattr(request, "sid"), data):
            disconnect()
            return

        start_presentation()


    @socketio.on("exit_presentation")
    def handle_exit_presentation(data=None):
        if not validate_socket_event(getattr(request, "sid"), data):
            disconnect()
            return

        exit_presentation()
