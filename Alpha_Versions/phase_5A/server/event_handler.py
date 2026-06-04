from phase_5A.server.mouse_controller import (
    move_mouse_relative
)


SENSITIVITY = 10


def handle_event(data):

    event_type = data.get("event")


    if event_type == "move":

        dx = data.get("dx")
        dy = data.get("dy")


        print(
            f"MOVE EVENT | dx={dx} | dy={dy}"
        )


        scaled_dx = int(dx * SENSITIVITY)
        scaled_dy = int(dy * SENSITIVITY)


        move_mouse_relative(
            scaled_dx,
            scaled_dy
        )