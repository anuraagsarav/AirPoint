from server.config import DEVELOPER_MODE
from server.security.key_manager import load_or_create_key
from server.security.security_logger import get_security_logger
from server.security.trusted_devices import load_trusted_devices


def initialize_security():
    get_security_logger()

    if not DEVELOPER_MODE:
        load_or_create_key()

    load_trusted_devices()
