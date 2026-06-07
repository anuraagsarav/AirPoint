import csv
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

from server.security.trusted_devices import (
    load_trusted_devices,
    remove_trusted_device
)


def show_trusted_devices_window():
    window = tk.Toplevel()
    window.title("Trusted Devices")
    window.geometry("860x420")
    window.minsize(760, 420)
    window.configure(bg="#111826")
    window.grid_rowconfigure(1, weight=1)
    window.grid_columnconfigure(0, weight=1)

    style = ttk.Style(window)

    style.configure(
        "Custom.Treeview",
        background="#17202a",
        foreground="#eef2fb",
        fieldbackground="#17202a",
        bordercolor="#1b2833",
        borderwidth=0,
        relief="flat",
        rowheight=30
    )
    style.configure(
        "Custom.Treeview.Heading",
        background="#1f2d40",
        foreground="#aab8d6",
        relief="flat",
        font=("Segoe UI", 10, "bold")
    )
    style.map(
        "Custom.Treeview.Heading",
        background=[("active", "#2b3b55")]
    )
    style.map(
        "Custom.Treeview",
        background=[("selected", "#4f6cff")],
        foreground=[("selected", "white")]
    )
    style.configure(
        "Accent.TButton",
        background="#4f6cff",
        foreground="white",
        borderwidth=0,
        focusthickness=0,
        padding=(12, 10),
        relief="flat"
    )
    style.layout(
        "Accent.TButton",
        [
            (
                "Button.border",
                {
                    "sticky": "nswe",
                    "children": [
                        (
                            "Button.padding",
                            {
                                "sticky": "nswe",
                                "children": [
                                    ("Button.label", {"sticky": "nswe"})
                                ]
                            }
                        )
                    ]
                }
            )
        ]
    )
    style.map(
        "Accent.TButton",
        background=[("active", "#6f7dff"), ("pressed", "#3c51a7"), ("!disabled", "#4f6cff")],
        foreground=[("disabled", "#a0aabd")]
    )
    style.configure(
        "Secondary.TButton",
        background="#1f2b3d",
        foreground="#d7e0f0",
        borderwidth=0,
        focusthickness=0,
        padding=(12, 10),
        relief="flat"
    )
    style.layout(
        "Secondary.TButton",
        [
            (
                "Button.border",
                {
                    "sticky": "nswe",
                    "children": [
                        (
                            "Button.padding",
                            {
                                "sticky": "nswe",
                                "children": [
                                    ("Button.label", {"sticky": "nswe"})
                                ]
                            }
                        )
                    ]
                }
            )
        ]
    )
    style.map(
        "Secondary.TButton",
        background=[("active", "#2b3a55"), ("pressed", "#1b2433")],
        foreground=[("disabled", "#7a8ba7")]
    )


    header_frame = tk.Frame(window, bg="#101823")
    header_frame.grid(row=0, column=0, sticky="ew", padx=16, pady=(16, 0))
    header_frame.grid_columnconfigure(0, weight=1)

    title = tk.Label(
        header_frame,
        text="Trusted Devices",
        font=("Segoe UI", 16, "bold"),
        fg="#eef2fb",
        bg="#101823"
    )
    title.grid(row=0, column=0, sticky="w")

    subtitle = tk.Label(
        header_frame,
        text="Manage devices that are allowed to connect to AirPoint.",
        font=("Segoe UI", 10),
        fg="#9aa4b2",
        bg="#101823"
    )
    subtitle.grid(row=1, column=0, sticky="w", pady=(6, 0))

    columns = (
        "device_name",
        "device_id",
        "first_seen",
        "last_seen"
    )

    table_frame = tk.Frame(window, bg="#111826")
    table_frame.grid(row=1, column=0, sticky="nsew", padx=16, pady=(12, 0))
    table_frame.grid_rowconfigure(0, weight=1)
    table_frame.grid_columnconfigure(0, weight=1)

    tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        style="Custom.Treeview"
    )

    tree.tag_configure("evenrow", background="#17202a")
    tree.tag_configure("oddrow", background="#1d2b3f")
    tree.tag_configure("selected", background="#4f6cff", foreground="white")

    headings = {
        "device_name": "Device Name",
        "device_id": "Device ID",
        "first_seen": "First Seen",
        "last_seen": "Last Seen"
    }

    for column, heading in headings.items():
        tree.heading(column, text=heading)
        tree.column(column, width=190, anchor="w")

    tree.grid(row=0, column=0, sticky="nsew")
    vsb = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    vsb.grid(row=0, column=1, sticky="ns")

    button_bar = tk.Frame(window, bg="#111826")
    button_bar.grid(row=2, column=0, sticky="ew", padx=16, pady=(12, 16))

    def refresh():
        for item in tree.get_children():
            tree.delete(item)

        for idx, device in enumerate(load_trusted_devices()["trusted_devices"]):
            tree.insert(
                "",
                "end",
                values=(
                    device.get("device_name", ""),
                    device.get("device_id", ""),
                    device.get("first_seen", ""),
                    device.get("last_seen", "")
                ),
                tags=("evenrow",) if idx % 2 == 0 else ("oddrow",)
            )

    def remove_selected():
        selected = tree.selection()

        if not selected:
            return

        values = tree.item(selected[0], "values")
        device_id = values[1]
        remove_trusted_device(device_id)
        refresh()

    def export_devices():
        file_path = filedialog.asksaveasfilename(
            title="Export Device List",
            defaultextension=".csv",
            filetypes=(("CSV files", "*.csv"),)
        )

        if not file_path:
            return

        devices = load_trusted_devices()["trusted_devices"]

        with open(file_path, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=columns)
            writer.writeheader()

            for device in devices:
                writer.writerow(
                    {
                        "device_name": device.get("device_name", ""),
                        "device_id": device.get("device_id", ""),
                        "first_seen": device.get("first_seen", ""),
                        "last_seen": device.get("last_seen", "")
                    }
                )

    tk.Button(
        button_bar,
        text="Remove Device",
        command=remove_selected,
        bg="#4f6cff",
        fg="white",
        activebackground="#6f7dff",
        activeforeground="white",
        bd=0,
        relief="flat",
        padx=12,
        pady=10,
        highlightthickness=0
    ).pack(side="left", padx=(0, 8))

    tk.Button(
        button_bar,
        text="Refresh",
        command=refresh,
        bg="#1f2b3d",
        fg="#d7e0f0",
        activebackground="#2b3a55",
        activeforeground="#eef2fb",
        bd=0,
        relief="flat",
        padx=12,
        pady=10,
        highlightthickness=0
    ).pack(side="left", padx=(0, 8))

    tk.Button(
        button_bar,
        text="Export Device List",
        command=export_devices,
        bg="#1f2b3d",
        fg="#d7e0f0",
        activebackground="#2b3a55",
        activeforeground="#eef2fb",
        bd=0,
        relief="flat",
        padx=12,
        pady=10,
        highlightthickness=0
    ).pack(side="left")

    refresh()
