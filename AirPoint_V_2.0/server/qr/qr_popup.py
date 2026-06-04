import tkinter as tk

from PIL import ImageTk
from PIL import Image

import qrcode

from io import BytesIO


# =========================================
# SHOW QR POPUP
# =========================================

def show_qr_popup(url):

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

    root.title("AirPoint V2.0")

    root.geometry("420x520")

    root.configure(bg="#0f1115")

    root.resizable(False, False)


    # =====================================
    # TITLE
    # =====================================

    title = tk.Label(

        root,

        text="AirPoint V2.0",

        font=("Arial", 22, "bold"),

        fg="white",

        bg="#0f1115"

    )

    title.pack(pady=(20, 10))


    # =====================================
    # SUBTITLE
    # =====================================

    subtitle = tk.Label(

        root,

        text="Scan QR from your phone",

        font=("Arial", 12),

        fg="#9aa4b2",

        bg="#0f1115"

    )

    subtitle.pack(pady=(0, 20))


    # =====================================
    # QR IMAGE
    # =====================================

    image = Image.open(buffer)

    image = image.resize((260, 260))

    photo = ImageTk.PhotoImage(image)


    qr_label = tk.Label(

        root,

        image=photo,

        bg="white"

    )

    qr_label.image = photo

    qr_label.pack(pady=10)


    # =====================================
    # URL TEXT
    # =====================================

    url_label = tk.Label(

        root,

        text=url,

        font=("Arial", 11),

        fg="#57d38c",

        bg="#0f1115",

        wraplength=360,

        justify="center"

    )

    url_label.pack(pady=20)


    # =====================================
    # FOOTER
    # =====================================

    footer = tk.Label(

        root,

        text="Phone and PC must be on same WiFi",

        font=("Arial", 10),

        fg="#7d8794",

        bg="#0f1115"

    )

    footer.pack(pady=(10, 0))


    root.mainloop()