import tkinter as tk
from tkinter import messagebox

from server.security.security_logger import log_warning
from server.security.trusted_devices import add_trusted_device


def request_device_approval(device_id, device_name, ip_address):
    root = tk.Tk()
    root.withdraw()

    message = (
        "New device requesting access.\n\n"
        f"Device Name:\n{device_name or 'Unknown Device'}\n\n"
        f"IP Address:\n{ip_address or 'Unknown'}\n\n"
        "Do you want to allow this device?"
    )

    allowed = messagebox.askyesno(
        "AirPoint Security Alert",
        message,
        parent=root
    )

    root.destroy()

    if allowed:
        add_trusted_device(device_id, device_name, ip_address)
        return True

    log_warning(
        "Unknown device rejected",
        device_id=device_id,
        device_name=device_name,
        ip_address=ip_address
    )
    return False
