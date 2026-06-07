import json
import secrets
import uuid
from pathlib import Path

from server.config import (
    SERVER_AUTH_DATA_FILE,
    LEGACY_SERVER_AUTH_TOKEN_FILE
)
from server.security.key_manager import get_fernet


def _load_or_create_auth_data():
    path = Path(SERVER_AUTH_DATA_FILE)

    if path.exists():
        try:
            decrypted = get_fernet().decrypt(path.read_bytes())
            data = json.loads(decrypted.decode("utf-8"))
            token = data.get("server_auth_token")
            server_id = data.get("server_id")
            if token and server_id:
                return token, server_id
        except Exception:
            pass

    legacy_path = Path(LEGACY_SERVER_AUTH_TOKEN_FILE)
    if legacy_path.exists():
        try:
            legacy_token = legacy_path.read_text(encoding="utf-8").strip()
            if legacy_token:
                server_id = uuid.uuid4().hex
                _save_auth_data(legacy_token, server_id)
                legacy_path.unlink(missing_ok=True)
                return legacy_token, server_id
        except OSError:
            pass

    token = secrets.token_urlsafe(32)
    server_id = uuid.uuid4().hex
    _save_auth_data(token, server_id)
    return token, server_id


def _save_auth_data(token, server_id):
    data = {
        "server_auth_token": token,
        "server_id": server_id
    }
    encrypted = get_fernet().encrypt(json.dumps(data).encode("utf-8"))
    Path(SERVER_AUTH_DATA_FILE).write_bytes(encrypted)


SERVER_AUTH_TOKEN, SERVER_ID = _load_or_create_auth_data()


def get_session_token():
    return SERVER_AUTH_TOKEN


def get_server_id():
    return SERVER_ID


def is_valid_session_token(token):
    return bool(token) and secrets.compare_digest(str(token), SERVER_AUTH_TOKEN)
