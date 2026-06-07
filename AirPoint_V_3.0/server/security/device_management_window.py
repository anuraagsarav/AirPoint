import csv
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

from server.security.trusted_devices import (
    load_trusted_devices,
    remove_trusted_device
)


# =========================================
# UTILITIES
# =========================================

def abbreviate_device_id(device_id):
    if not device_id:
        return ""

    device_id = str(device_id)

    if len(device_id) <= 22:
        return device_id

    return f"{device_id[:12]}...{device_id[-8:]}"


# =========================================
# TRUSTED DEVICES WINDOW
# =========================================

def show_trusted_devices_window():

    window = tk.Toplevel()

    window.title("Trusted Devices")
    window.minsize(860, 500)
    window.configure(bg="#111826")

    window.grid_rowconfigure(1, weight=1)
    window.grid_columnconfigure(0, weight=1)

    window.update_idletasks()

    width = 980
    height = 560

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    window.geometry(f"{width}x{height}+{x}+{y}")

    # =====================================
    # STYLES
    # =====================================

    style = ttk.Style(window)

    style.theme_use("default")

    style.configure(
        "Custom.Treeview",
        background="#17202a",
        foreground="#eef2fb",
        fieldbackground="#17202a",
        borderwidth=0,
        rowheight=34,
        font=("Segoe UI", 10)
    )

    style.configure(
        "Custom.Treeview.Heading",
        background="#1f2d40",
        foreground="#c5d1ea",
        relief="flat",
        font=("Segoe UI", 10, "bold")
    )

    style.map(
        "Custom.Treeview",
        background=[("selected", "#4f6cff")],
        foreground=[("selected", "white")]
    )

    style.map(
        "Custom.Treeview.Heading",
        background=[("active", "#2c3f5c")]
    )

    # =====================================
    # HEADER
    # =====================================

    header_frame = tk.Frame(
        window,
        bg="#101823"
    )

    header_frame.grid(
        row=0,
        column=0,
        sticky="ew",
        padx=20,
        pady=(18, 0)
    )

    header_frame.grid_columnconfigure(
        0,
        weight=1
    )

    title_label = tk.Label(
        header_frame,
        text="Trusted Devices",
        font=("Segoe UI", 18, "bold"),
        fg="#eef2fb",
        bg="#101823"
    )

    title_label.grid(
        row=0,
        column=0,
        sticky="w"
    )

    subtitle = tk.Label(
        header_frame,
        text="Manage devices that are allowed to connect to AirPoint.",
        font=("Segoe UI", 10),
        fg="#9aa4b2",
        bg="#101823"
    )

    subtitle.grid(
        row=1,
        column=0,
        sticky="w",
        pady=(6, 0)
    )

    # =====================================
    # TABLE CARD
    # =====================================

    table_frame = tk.Frame(
        window,
        bg="#111826"
    )

    table_frame.grid(
        row=1,
        column=0,
        sticky="nsew",
        padx=20,
        pady=(12, 0)
    )

    table_frame.grid_rowconfigure(
        0,
        weight=1
    )

    table_frame.grid_columnconfigure(
        0,
        weight=1
    )

    columns = (
        "device_name",
        "device_id",
        "first_seen",
        "last_seen"
    )

    tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        style="Custom.Treeview"
    )

    tree.heading(
        "device_name",
        text="Device"
    )

    tree.heading(
        "device_id",
        text="Device ID"
    )

    tree.heading(
        "first_seen",
        text="First Seen"
    )

    tree.heading(
        "last_seen",
        text="Last Active"
    )

    tree.column(
        "device_name",
        width=180,
        anchor="w"
    )

    tree.column(
        "device_id",
        width=240,
        anchor="w"
    )

    tree.column(
        "first_seen",
        width=220,
        anchor="center"
    )

    tree.column(
        "last_seen",
        width=220,
        anchor="center"
    )

    tree.tag_configure(
        "evenrow",
        background="#17202a"
    )

    tree.tag_configure(
        "oddrow",
        background="#1d2b3f"
    )

    tree.grid(
        row=0,
        column=0,
        sticky="nsew"
    )

    scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=tree.yview
    )

    tree.configure(
        yscrollcommand=scrollbar.set
    )

    scrollbar.grid(
        row=0,
        column=1,
        sticky="ns"
    )

    empty_label = tk.Label(
        table_frame,
        text="🔒 No Trusted Devices\n\nApproved devices will appear here.",
        bg="#111826",
        fg="#8fa2c7",
        font=("Segoe UI", 12),
        justify="center"
    )

    # =====================================
    # ACTIONS
    # =====================================

    def refresh():

        for item in tree.get_children():
            tree.delete(item)

        devices = load_trusted_devices()["trusted_devices"]

        title_label.config(
            text=f"Trusted Devices ({len(devices)})"
        )

        if not devices:
            empty_label.place(
                relx=0.5,
                rely=0.5,
                anchor="center"
            )
        else:
            empty_label.place_forget()

        for idx, device in enumerate(devices):

            tree.insert(
                "",
                "end",
                values=(
                    device.get("device_name", ""),
                    abbreviate_device_id(
                        device.get("device_id", "")
                    ),
                    device.get("first_seen", ""),
                    device.get("last_seen", "")
                ),
                tags=(
                    "evenrow",
                ) if idx % 2 == 0 else (
                    "oddrow",
                )
            )

    def remove_selected():

        selected = tree.selection()

        if not selected:
            return

        values = tree.item(
            selected[0],
            "values"
        )

        short_id = values[1]

        devices = load_trusted_devices()["trusted_devices"]

        real_device_id = None

        for device in devices:

            abbreviated = abbreviate_device_id(
                device.get("device_id", "")
            )

            if abbreviated == short_id:
                real_device_id = device.get(
                    "device_id",
                    ""
                )
                break

        if real_device_id:
            remove_trusted_device(
                real_device_id
            )

        refresh()

    def export_devices():

        file_path = filedialog.asksaveasfilename(
            title="Export Device List",
            defaultextension=".csv",
            filetypes=(
                ("CSV Files", "*.csv"),
            )
        )

        if not file_path:
            return

        devices = load_trusted_devices()["trusted_devices"]

        with open(
            file_path,
            "w",
            newline="",
            encoding="utf-8"
        ) as csv_file:

            writer = csv.DictWriter(
                csv_file,
                fieldnames=columns
            )

            writer.writeheader()

            for device in devices:

                writer.writerow(
                    {
                        "device_name": device.get(
                            "device_name",
                            ""
                        ),
                        "device_id": device.get(
                            "device_id",
                            ""
                        ),
                        "first_seen": device.get(
                            "first_seen",
                            ""
                        ),
                        "last_seen": device.get(
                            "last_seen",
                            ""
                        )
                    }
                )

    # =====================================
    # BUTTON BAR
    # =====================================

    button_bar = tk.Frame(
        window,
        bg="#111826"
    )

    button_bar.grid(
        row=2,
        column=0,
        sticky="ew",
        padx=20,
        pady=(14, 18)
    )

    left_buttons = tk.Frame(
        button_bar,
        bg="#111826"
    )

    left_buttons.pack(
        side="left"
    )

    tk.Button(
        left_buttons,
        text="Refresh",
        command=refresh,
        bg="#1f2b3d",
        fg="#d7e0f0",
        activebackground="#2b3a55",
        activeforeground="#ffffff",
        relief="flat",
        bd=0,
        padx=16,
        pady=10,
        cursor="hand2"
    ).pack(
        side="left",
        padx=(0, 8)
    )

    tk.Button(
        left_buttons,
        text="Export Device List",
        command=export_devices,
        bg="#1f2b3d",
        fg="#d7e0f0",
        activebackground="#2b3a55",
        activeforeground="#ffffff",
        relief="flat",
        bd=0,
        padx=16,
        pady=10,
        cursor="hand2"
    ).pack(
        side="left"
    )

    tk.Button(
        button_bar,
        text="Remove Device",
        command=remove_selected,
        bg="#c0392b",
        fg="white",
        activebackground="#e74c3c",
        activeforeground="white",
        relief="flat",
        bd=0,
        padx=16,
        pady=10,
        cursor="hand2"
    ).pack(
        side="right"
    )

    refresh()