# ==========================================
# CURRENT MODE
# ==========================================

current_mode = "normal"


# ==========================================
# SET MODE
# ==========================================

def set_mode(mode):

    global current_mode

    current_mode = mode

    """print(
         f"\nMode changed to: {mode}"
    )"""


# ==========================================
# GET MODE
# ==========================================

def get_mode():

    return current_mode