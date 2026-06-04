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

    columns = (
        "device_name",
        "device_id",
        "first_seen",
        "last_seen"
    )

    tree = ttk.Treeview(
        window,
        columns=columns,
        show="headings"
    )

    headings = {
        "device_name": "Device Name",
        "device_id": "Device ID",
        "first_seen": "First Seen",
        "last_seen": "Last Seen"
    }

    for column, heading in headings.items():
        tree.heading(column, text=heading)
        tree.column(column, width=190, anchor="w")

    tree.pack(fill="both", expand=True, padx=12, pady=(12, 8))

    button_bar = tk.Frame(window)
    button_bar.pack(fill="x", padx=12, pady=(0, 12))

    def refresh():
        for item in tree.get_children():
            tree.delete(item)

        for device in load_trusted_devices()["trusted_devices"]:
            tree.insert(
                "",
                "end",
                values=(
                    device.get("device_name", ""),
                    device.get("device_id", ""),
                    device.get("first_seen", ""),
                    device.get("last_seen", "")
                )
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
        command=remove_selected
    ).pack(side="left", padx=(0, 8))

    tk.Button(
        button_bar,
        text="Refresh",
        command=refresh
    ).pack(side="left", padx=(0, 8))

    tk.Button(
        button_bar,
        text="Export Device List",
        command=export_devices
    ).pack(side="left")

    refresh()
