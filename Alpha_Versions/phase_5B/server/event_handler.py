from math import sqrt

from phase_5B.server.mouse_controller import (

    move_mouse_relative,

    left_click,

    right_click
)


# =====================================
# BASE SETTINGS
# =====================================

BASE_SENSITIVITY = 2.5

DEADZONE = 1


# =====================================
# SMOOTHING SETTINGS
# =====================================

movement_history = []

MAX_HISTORY = 5


# =====================================
# ACCELERATION SETTINGS
# =====================================

ACCELERATION_MULTIPLIER = 0.08

MAX_ACCELERATION = 3


# =====================================
# MAIN EVENT HANDLER
# =====================================

def handle_event(data):

    global movement_history


    event_type = data.get("event")


    # =====================================
    # MOUSE MOVEMENT
    # =====================================

    if event_type == "move":

        dx = data.get("dx")
        dy = data.get("dy")


        # =====================================
        # DEADZONE FILTER
        # =====================================

        if abs(dx) < DEADZONE:

            dx = 0


        if abs(dy) < DEADZONE:

            dy = 0


        # =====================================
        # STORE MOVEMENT HISTORY
        # =====================================

        movement_history.append((dx, dy))


        # =====================================
        # LIMIT HISTORY SIZE
        # =====================================

        if len(movement_history) > MAX_HISTORY:

            movement_history.pop(0)


        # =====================================
        # MOVING AVERAGE SMOOTHING
        # =====================================

        avg_dx = sum(x for x, y in movement_history) / len(movement_history)

        avg_dy = sum(y for x, y in movement_history) / len(movement_history)


        # =====================================
        # VELOCITY CALCULATION
        # =====================================

        velocity = sqrt(
            avg_dx ** 2 +
            avg_dy ** 2
        )


        # =====================================
        # DYNAMIC ACCELERATION
        # =====================================

        acceleration = 1 + (
            velocity *
            ACCELERATION_MULTIPLIER
        )


        # =====================================
        # LIMIT MAX ACCELERATION
        # =====================================

        acceleration = min(
            acceleration,
            MAX_ACCELERATION
        )


        # =====================================
        # APPLY FINAL SENSITIVITY
        # =====================================

        final_dx = int(
            avg_dx *
            BASE_SENSITIVITY *
            acceleration
        )


        final_dy = int(
            avg_dy *
            BASE_SENSITIVITY *
            acceleration
        )


        # =====================================
        # MOVE CURSOR
        # =====================================

        move_mouse_relative(
            final_dx,
            final_dy
        )


    # =====================================
    # LEFT CLICK
    # =====================================

    elif event_type == "left_click":

        print("LEFT CLICK")

        left_click()


    # =====================================
    # RIGHT CLICK
    # =====================================

    elif event_type == "right_click":

        print("RIGHT CLICK")

        right_click()