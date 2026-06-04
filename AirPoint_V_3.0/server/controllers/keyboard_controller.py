import ctypes


# ==========================================
# WINDOWS USER32
# ==========================================

user32 = ctypes.windll.user32


# ==========================================
# KEYBOARD CONSTANTS
# ==========================================

KEYEVENTF_KEYUP = 0x0002


# ==========================================
# VIRTUAL KEY CODES
# ==========================================

VK_LEFT = 0x25
VK_RIGHT = 0x27

VK_F5 = 0x74
VK_ESCAPE = 0x1B


# ==========================================
# PRESS KEY
# ==========================================

def press_key(key_code):

    user32.keybd_event(
        key_code,
        0,
        0,
        0
    )

    user32.keybd_event(
        key_code,
        0,
        KEYEVENTF_KEYUP,
        0
    )


# ==========================================
# NEXT SLIDE
# ==========================================

def next_slide():

    press_key(VK_RIGHT)


# ==========================================
# PREVIOUS SLIDE
# ==========================================

def previous_slide():

    press_key(VK_LEFT)


# ==========================================
# START SLIDESHOW
# ==========================================

def start_slideshow():

    press_key(VK_F5)


# ==========================================
# EXIT SLIDESHOW
# ==========================================

def exit_slideshow():

    press_key(VK_ESCAPE)