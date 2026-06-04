from math import log

from server.config import (
    ACCELERATION_FACTOR,
    MAX_ACCELERATION,
)


def calculate_acceleration(velocity):

    acceleration = (1 + log(velocity + 1) * ACCELERATION_FACTOR)

    return min(
        acceleration,
        MAX_ACCELERATION
    )