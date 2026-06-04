import ctypes
import time

user32 = ctypes.windll.user32

MOUSEEVENTF_MOVE = 0x0001

MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004

MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010

MOUSEEVENTF_WHEEL = 0x0800

device_fractional_parts = {}

def move_mouse_relative(dx, dy, device_id=None):

    if device_id and device_id not in device_fractional_parts:
        device_fractional_parts[device_id] = {"x": 0.0, "y": 0.0}

    if device_id:
        frac = device_fractional_parts[device_id]
        dx += frac["x"]
        dy += frac["y"]

    int_dx = int(dx)
    int_dy = int(dy)

    if device_id:
        device_fractional_parts[device_id]["x"] = dx - int_dx
        device_fractional_parts[device_id]["y"] = dy - int_dy

    user32.mouse_event(
        MOUSEEVENTF_MOVE,
        int_dx,
        int_dy,
        0,
        0
    )

def left_click():

    user32.mouse_event(
        MOUSEEVENTF_LEFTDOWN,
        0,
        0,
        0,
        0
    )

    time.sleep(0.01)

    user32.mouse_event(
        MOUSEEVENTF_LEFTUP,
        0,
        0,
        0,
        0
    )

def right_click():

    user32.mouse_event(
        MOUSEEVENTF_RIGHTDOWN,
        0,
        0,
        0,
        0
    )

    time.sleep(0.03)

    user32.mouse_event(
        MOUSEEVENTF_RIGHTUP,
        0,
        0,
        0,
        0
    )


def scroll_vertical(amount):

    user32.mouse_event(
        MOUSEEVENTF_WHEEL,
        0,
        0,
        int(amount),
        0
    )


def clear_device_state(device_id):
    if device_id in device_fractional_parts:
        del device_fractional_parts[device_id]

    