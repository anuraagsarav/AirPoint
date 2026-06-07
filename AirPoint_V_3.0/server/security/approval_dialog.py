import tkinter as tk

from server.security.security_logger import log_warning
from server.security.trusted_devices import add_trusted_device


def request_device_approval(device_id, device_name, ip_address):

    result = {"allowed": False}

    window = tk.Tk()

    window.title("AirPoint Security Alert")
    window.geometry("420x360")
    window.resizable(False, False)
    window.configure(bg="#111826")

    window.eval("tk::PlaceWindow . center")

    # =====================================
    # MAIN CARD
    # =====================================

    card = tk.Frame(
        window,
        bg="#1a2436"
    )

    card.pack(
        fill="both",
        expand=True,
        padx=12,
        pady=12
    )

    # =====================================
    # HEADER
    # =====================================

    tk.Label(
        card,
        text="⚠ AirPoint Security Alert",
        bg="#1a2436",
        fg="white",
        font=("Segoe UI", 16, "bold")
    ).pack(
        pady=(18, 8)
    )

    tk.Label(
        card,
        text="A new device is requesting access",
        bg="#1a2436",
        fg="#b7c3d7",
        font=("Segoe UI", 10)
    ).pack(
        pady=(0, 15)
    )

    # =====================================
    # DEVICE CARD
    # =====================================

    info_card = tk.Frame(
        card,
        bg="#162033"
    )

    info_card.pack(
        fill="x",
        padx=20,
        pady=(0, 15)
    )

    tk.Label(
        info_card,
        text="DEVICE NAME",
        bg="#162033",
        fg="#98a6c0",
        font=("Segoe UI", 8, "bold")
    ).pack(
        anchor="w",
        padx=12,
        pady=(10, 0)
    )

    tk.Label(
        info_card,
        text=device_name or "Unknown Device",
        bg="#162033",
        fg="white",
        font=("Segoe UI", 11)
    ).pack(
        anchor="w",
        padx=12,
        pady=(0, 8)
    )

    tk.Label(
        info_card,
        text="IP ADDRESS",
        bg="#162033",
        fg="#98a6c0",
        font=("Segoe UI", 8, "bold")
    ).pack(
        anchor="w",
        padx=12
    )

    tk.Label(
        info_card,
        text=ip_address or "Unknown",
        bg="#162033",
        fg="white",
        font=("Segoe UI", 11)
    ).pack(
        anchor="w",
        padx=12,
        pady=(0, 12)
    )

    # =====================================
    # QUESTION
    # =====================================

    tk.Label(
        card,
        text="Allow this device to connect?",
        bg="#1a2436",
        fg="#d7e0f0",
        font=("Segoe UI", 10)
    ).pack(
        pady=(0, 15)
    )

    # =====================================
    # BUTTONS
    # =====================================

    button_frame = tk.Frame(
        card,
        bg="#1a2436"
    )

    button_frame.pack(
        pady=(0, 15)
    )

    def approve():
        result["allowed"] = True
        window.destroy()

    def deny():
        result["allowed"] = False
        window.destroy()

    tk.Button(
        button_frame,
        text="Deny",
        command=deny,
        bg="#2b3547",
        fg="white",
        activebackground="#394860",
        activeforeground="white",
        relief="flat",
        bd=0,
        width=14,
        pady=8,
        cursor="hand2"
    ).pack(
        side="left",
        padx=6
    )

    tk.Button(
        button_frame,
        text="Approve",
        command=approve,
        bg="#4f6cff",
        fg="white",
        activebackground="#6f7dff",
        activeforeground="white",
        relief="flat",
        bd=0,
        width=14,
        pady=8,
        cursor="hand2"
    ).pack(
        side="left",
        padx=6
    )

    # =====================================
    # CLOSE HANDLER
    # =====================================

    window.protocol(
        "WM_DELETE_WINDOW",
        deny
    )

    window.mainloop()

    if result["allowed"]:
        add_trusted_device(
            device_id,
            device_name,
            ip_address
        )
        return True

    log_warning(
        "Unknown device rejected",
        device_id=device_id,
        device_name=device_name,
        ip_address=ip_address
    )

    return False
