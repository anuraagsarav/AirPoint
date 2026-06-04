from threading import Lock

from server.security.session_token import is_valid_session_token
from server.security.security_logger import log_warning
from server.security.trusted_devices import is_trusted_device


_authorized_connections = {}
_lock = Lock()


def register_authorized_connection(sid, device_id):
    with _lock:
        _authorized_connections[sid] = device_id


def remove_authorized_connection(sid):
    with _lock:
        _authorized_connections.pop(sid, None)


def get_authorized_device_id(sid):
    with _lock:
        return _authorized_connections.get(sid)


def is_socket_authorized(sid):
    device_id = get_authorized_device_id(sid)

    return bool(device_id) and is_trusted_device(device_id)


def validate_socket_event(sid, data=None):
    if not is_socket_authorized(sid):
        log_warning("Unauthorized socket event", sid=sid)
        return False

    if not isinstance(data, dict):
        log_warning("Invalid session token", sid=sid)
        return False

    token = data.get("token")
    if not is_valid_session_token(token):
        log_warning("Invalid session token", sid=sid)
        return False

    return True
