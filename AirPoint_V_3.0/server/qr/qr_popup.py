import tkinter as tk
from tkinter import ttk

from PIL import ImageTk
from PIL import Image

import qrcode

from io import BytesIO

from server.security.device_management_window import (
    show_trusted_devices_window
)


# =========================================
# UTILITIES
# =========================================

def abbreviate_server_id(server_id):
    if not server_id:
        return None

    if len(server_id) <= 16:
        return server_id

    return f"{server_id[:8]}…{server_id[-4:]}"


# =========================================
# SHOW QR POPUP
# =========================================

def show_qr_popup(url, server_id=None):

    # =====================================
    # GENERATE QR
    # =====================================

    qr = qrcode.make(url)

    buffer = BytesIO()

    qr.save(

        buffer,

        format="PNG"

    )

    buffer.seek(0)


    # =====================================
    # TKINTER WINDOW
    # =====================================

    root = tk.Tk()

    root.title("AirPoint V3.0")
    root.geometry("440x560")
    root.resizable(False, False)
    root.configure(bg="#12151d")
    root.eval("tk::PlaceWindow . center")

    root.option_add("*Menu.background", "#1f2633")
    root.option_add("*Menu.foreground", "#f5f7fb")
    root.option_add("*Menu.activeBackground", "#2b3550")
    root.option_add("*Menu.activeForeground", "#ffffff")

    style = ttk.Style(root)
    style.configure("Card.TFrame", background="#1f2633")
    style.configure("Title.TLabel", background="#1f2633", foreground="#f5f7fb", font=("Segoe UI", 20, "bold"))
    style.configure("Subtitle.TLabel", background="#1f2633", foreground="#a1afcc", font=("Segoe UI", 11))
    style.configure("Url.TLabel", background="#1f2633", foreground="#8ec9ff", font=("Segoe UI", 10), wraplength=380, justify="center")
    style.configure("Footer.TLabel", background="#12151d", foreground="#8a98b8", font=("Segoe UI", 9))
    style.configure("DarkButton.TButton", background="#2b3550", foreground="#f5f7fb", font=("Segoe UI", 10), borderwidth=0)
    style.map("DarkButton.TButton",
        background=[("active", "#3a4a70"), ("pressed", "#263251")],
        foreground=[("disabled", "#7a8ba7")]
    )

    menu_bar = tk.Menu(root)
    menu_bar.add_command(
        label="Trusted Devices",
        command=show_trusted_devices_window
    )
    root.config(menu=menu_bar)

    content = ttk.Frame(root, style="Card.TFrame", padding=(20, 18, 20, 20))
    content.pack(expand=True, fill="both", padx=16, pady=16)

    title = ttk.Label(
        content,
        text="AirPoint V3.0",
        style="Title.TLabel"
    )
    title.pack(pady=(0, 6))

    subtitle = ttk.Label(
        content,
        text="Scan the QR code with your phone",
        style="Subtitle.TLabel"
    )
    subtitle.pack(pady=(0, 10))

    if server_id:
        server_label = ttk.Label(
            content,
            text=f"Server ID: {abbreviate_server_id(server_id)}",
            style="Subtitle.TLabel"
        )
        server_label.pack(pady=(0, 18))
    else:
        subtitle.pack_configure(pady=(0, 18))


    # =====================================
    # QR IMAGE
    # =====================================

    image = Image.open(buffer)
    image = image.resize((260, 260))
    photo = ImageTk.PhotoImage(image)

    qr_frame = ttk.Frame(content, style="Card.TFrame", padding=12)
    qr_frame.pack(pady=(0, 12))

    qr_label = tk.Label(
        qr_frame,
        image=photo,
        bg="#1f2633",
        relief="flat",
        bd=0
    )
    qr_label.image = photo
    qr_label.pack(padx=4, pady=4)

    # =====================================
    # URL TEXT
    # =====================================

    url_label = ttk.Label(
        content,
        text=url,
        style="Url.TLabel"
    )
    url_label.pack(pady=(10, 18))

    # =====================================
    # FOOTER
    # =====================================

    footer = ttk.Label(
        root,
        text="Phone and PC must be on same WiFi",
        style="Footer.TLabel"
    )
    footer.pack(side="bottom", pady=(0, 14))

    root.mainloop()
