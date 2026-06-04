from pathlib import Path
import sys

from cryptography.fernet import Fernet

from server.config import SECURITY_KEY_FILE


DPAPI_KEY_PREFIX = b"AIRPOINT_DPAPI_KEY_V1\n"


def load_or_create_key():
    key_path = Path(SECURITY_KEY_FILE)

    if key_path.exists():
        stored_key = key_path.read_bytes()
        return _load_existing_key(stored_key, key_path)

    key = Fernet.generate_key()
    _write_key_file(key_path, key)

    return key


def get_fernet():
    return Fernet(load_or_create_key())


def _load_existing_key(stored_key, key_path):
    if stored_key.startswith(DPAPI_KEY_PREFIX):
        return _unprotect_key(stored_key[len(DPAPI_KEY_PREFIX):])

    # Existing V3 installs may already have a raw Fernet key. Use it once,
    # validate it, then immediately rewrite it as a DPAPI-protected key.
    Fernet(stored_key)
    _write_key_file(key_path, stored_key)

    return stored_key


def _write_key_file(key_path, key):
    if _is_windows():
        protected_key = _protect_key(key)
        key_path.write_bytes(DPAPI_KEY_PREFIX + protected_key)
        return

    key_path.write_bytes(key)


def _protect_key(key):
    from server.security.windows_dpapi import protect_data

    return protect_data(key)


def _unprotect_key(protected_key):
    from server.security.windows_dpapi import unprotect_data

    return unprotect_data(protected_key)


def _is_windows():
    return sys.platform.startswith("win")
