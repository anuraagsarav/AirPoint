from math import sqrt

from server.config import (
    BASE_SENSITIVITY,
    SMOOTHING_ALPHA,
    DEADZONE
)

from server.controllers.mouse_controller import (
    move_mouse_relative
)

from server.input_engine.smoothing_engine import (
    smooth_movement
)

from server.input_engine.acceleration_engine import (
    calculate_acceleration
)

def process_movement(data, device_id):

    dx = data.get("dx", 0)
    dy = data.get("dy", 0)

    if abs(dx) < DEADZONE:
        dx = 0

    if abs(dy) < DEADZONE:
        dy = 0

    smoothed_dx, smoothed_dy = smooth_movement(dx, dy, SMOOTHING_ALPHA, device_id)

    velocity = sqrt(smoothed_dx ** 2 + smoothed_dy ** 2)

    acceleration = calculate_acceleration(velocity)

    final_dx = (smoothed_dx * BASE_SENSITIVITY * acceleration)
    final_dy = (smoothed_dy * BASE_SENSITIVITY * acceleration)

    move_mouse_relative(final_dx, final_dy, device_id)

