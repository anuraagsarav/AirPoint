device_states = {}

def smooth_movement(dx, dy, alpha, device_id):

    if device_id not in device_states:
        device_states[device_id] = {
            "previous_dx": 0,
            "previous_dy": 0
        }

    state = device_states[device_id]

    smoothed_dx = (
        state["previous_dx"] +
        alpha * (dx - state["previous_dx"])
    )

    smoothed_dy = (
        state["previous_dy"] +
        alpha * (dy - state["previous_dy"])
    )

    state["previous_dx"] = smoothed_dx
    state["previous_dy"] = smoothed_dy

    return smoothed_dx, smoothed_dy


def clear_device_state(device_id):
    if device_id in device_states:
        del device_states[device_id]



