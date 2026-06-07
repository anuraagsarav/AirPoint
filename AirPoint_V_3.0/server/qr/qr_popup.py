import tkinter as tk

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
        return ""

    if len(server_id) <= 20:
        return server_id

    return f"{server_id[:8]}...{server_id[-4:]}"


def abbreviate_pairing_link(url):
    if not url:
        return ""

    url = str(url)

    if "?" not in url:
        return url

    base_url, query = url.split("?", 1)

    if len(query) <= 24:
        return url

    return f"{base_url}?{query[:12]}...{query[-10:]}"


# =========================================
# SHOW QR POPUP
# =========================================

def show_qr_popup(url, server_id=None):

    display_url = abbreviate_pairing_link(url)

    # =====================================
    # GENERATE QR
    # =====================================

    qr = qrcode.make(url)

    buffer = BytesIO()

    qr.save(
        buffer,
        format="PNG"  # type: ignore
    )

    buffer.seek(0)

    # =====================================
    # WINDOW
    # =====================================

    root = tk.Tk()

    root.title("AirPoint V3.0")
    root.geometry("460x560")
    root.resizable(False, False)
    root.configure(bg="#111826")

    root.eval("tk::PlaceWindow . center")

    # =====================================
    # COPY UTILITIES
    # =====================================

    def copy_pairing_link():
        root.clipboard_clear()
        root.clipboard_append(str(url))
        root.update()

    def copy_server_id():
        if server_id:
            root.clipboard_clear()
            root.clipboard_append(str(server_id))
            root.update()

    # =====================================
    # MENU
    # =====================================

    menu_bar = tk.Menu(root)

    menu_bar.add_command(
        label="Trusted Devices",
        command=show_trusted_devices_window
    )

    root.config(menu=menu_bar)

    # =====================================
    # MAIN CARD
    # =====================================

    card = tk.Frame(
        root,
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
        text="AirPoint V3.0",
        bg="#1a2436",
        fg="white",
        font=("Segoe UI", 20, "bold")
    ).pack(
        pady=(12, 4)
    )

    tk.Label(
        card,
        text="Scan the QR code with your phone",
        bg="#1a2436",
        fg="#b7c3d7",
        font=("Segoe UI", 10)
    ).pack(
        pady=(0, 10)
    )

    # =====================================
    # QR CODE
    # =====================================

    image = Image.open(buffer)
    image = image.resize((200, 200))

    photo = ImageTk.PhotoImage(image)

    qr_frame = tk.Frame(
        card,
        bg="#24334f",
        padx=1,
        pady=1
    )

    qr_frame.pack(
        pady=(0, 10)
    )

    qr_label = tk.Label(
        qr_frame,
        image=photo,
        bg="white",
        bd=0
    )

    qr_label.image = photo  # type: ignore[attr-defined]

    qr_label.pack()

    # =====================================
    # SERVER ID CARD
    # =====================================

    if server_id:

        session_card = tk.Frame(
            card,
            bg="#162033"
        )

        session_card.pack(
            fill="x",
            padx=20,
            pady=(0, 6)
        )

        tk.Label(
            session_card,
            text="SERVER ID",
            bg="#162033",
            fg="#98a6c0",
            font=("Segoe UI", 8, "bold")
        ).pack(
            pady=(8, 2)
        )

        tk.Label(
            session_card,
            text=abbreviate_server_id(server_id),
            bg="#162033",
            fg="#4f6cff",
            font=("Segoe UI", 13, "bold")
        ).pack(
            pady=(0, 6)
        )


    # =====================================
    # PAIRING LINK CARD
    # =====================================

    url_card = tk.Frame(
        card,
        bg="#162033"
    )

    url_card.pack(
        fill="x",
        padx=20,
        pady=(0, 10)
    )

    tk.Label(
        url_card,
        text="PAIRING LINK",
        bg="#162033",
        fg="#98a6c0",
        font=("Segoe UI", 8, "bold")
    ).pack(
        pady=(8, 2)
    )

    tk.Label(
        url_card,
        text=display_url,
        bg="#162033",
        fg="#8ec9ff",
        font=("Consolas", 8),
        wraplength=360,
        justify="center"
    ).pack(
        padx=10,
        pady=(0, 6)
    )

    tk.Button(
        url_card,
        text="Copy Connection Link",
        command=copy_pairing_link,
        bg="#4f6cff",
        fg="white",
        activebackground="#6f7dff",
        activeforeground="white",
        relief="flat",
        bd=0,
        cursor="hand2"
    ).pack(
        pady=(0, 8)
    )

    # =====================================
    # FOOTER
    # =====================================

    footer = tk.Frame(
        root,
        bg="#111826"
    )

    footer.pack(
        fill="x",
        pady=(0, 6)
    )

    tk.Label(
        footer,
        text="✓ Same WiFi Network Required",
        bg="#111826",
        fg="#8a98b8",
        font=("Segoe UI", 8)
    ).pack()

    tk.Label(
        footer,
        text="✓ Secure Device Authentication",
        bg="#111826",
        fg="#8a98b8",
        font=("Segoe UI", 8)
    ).pack()

    root.mainloop()
