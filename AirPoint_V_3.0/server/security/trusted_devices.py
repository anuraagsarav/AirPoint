import json
from datetime import datetime
from pathlib import Path

from server.config import (
    DEVELOPER_MODE,
    TRUSTED_DEVICES_ENC,
    TRUSTED_DEVICES_JSON
)
from server.security.key_manager import get_fernet
from server.security.security_logger import log_info


EMPTY_STORE = {
    "trusted_devices": []
}


def utc_now_iso():
    return datetime.utcnow().replace(microsecond=0).isoformat()


def load_trusted_devices():
    if DEVELOPER_MODE:
        return _load_json_store()

    return _load_encrypted_store()


def save_trusted_devices(data):
    normalized = _normalize_store(data)

    if DEVELOPER_MODE:
        _json_path().write_text(
            json.dumps(normalized, indent=2),
            encoding="utf-8"
        )
        return

    if _json_path().exists():
        _json_path().unlink()

    encrypted = get_fernet().encrypt(
        json.dumps(normalized).encode("utf-8")
    )
    _enc_path().write_bytes(encrypted)


def add_trusted_device(device_id, device_name, ip_address=None):
    data = load_trusted_devices()
    devices = data["trusted_devices"]
    now = utc_now_iso()

    for device in devices:
        if device.get("device_id") == device_id:
            device["device_name"] = device_name or device.get("device_name")
            device["last_seen"] = now
            if ip_address:
                device["last_ip"] = ip_address
            save_trusted_devices(data)
            return device

    device = {
        "device_id": device_id,
        "device_name": device_name or "Unknown Device",
        "first_seen": now,
        "last_seen": now
    }

    if ip_address:
        device["last_ip"] = ip_address

    devices.append(device)
    save_trusted_devices(data)
    log_info("Device approved", device_id=device_id, device_name=device_name)

    return device


def remove_trusted_device(device_id):
    data = load_trusted_devices()
    before = len(data["trusted_devices"])
    data["trusted_devices"] = [
        device
        for device in data["trusted_devices"]
        if device.get("device_id") != device_id
    ]

    removed = len(data["trusted_devices"]) != before

    if removed:
        save_trusted_devices(data)
        log_info("Trusted device removed", device_id=device_id)

    return removed


def is_trusted_device(device_id):
    if not device_id:
        return False

    data = load_trusted_devices()

    return any(
        device.get("device_id") == device_id
        for device in data["trusted_devices"]
    )


def update_last_seen(device_id, ip_address=None):
    data = load_trusted_devices()
    now = utc_now_iso()

    for device in data["trusted_devices"]:
        if device.get("device_id") == device_id:
            device["last_seen"] = now
            if ip_address:
                device["last_ip"] = ip_address
            save_trusted_devices(data)
            return device

    return None


def _load_json_store():
    path = _json_path()

    if not path.exists():
        save_trusted_devices(EMPTY_STORE)

    try:
        return _normalize_store(
            json.loads(path.read_text(encoding="utf-8"))
        )
    except (json.JSONDecodeError, OSError):
        return EMPTY_STORE.copy()


def _load_encrypted_store():
    path = _enc_path()

    if not path.exists():
        save_trusted_devices(EMPTY_STORE)

    try:
        decrypted = get_fernet().decrypt(path.read_bytes())
        return _normalize_store(
            json.loads(decrypted.decode("utf-8"))
        )
    except Exception:
        return EMPTY_STORE.copy()


def _normalize_store(data):
    if not isinstance(data, dict):
        return EMPTY_STORE.copy()

    devices = data.get("trusted_devices", [])

    if not isinstance(devices, list):
        devices = []

    return {
        "trusted_devices": devices
    }


def _json_path():
    return Path(TRUSTED_DEVICES_JSON)


def _enc_path():
    return Path(TRUSTED_DEVICES_ENC)
