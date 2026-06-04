from server.controllers.mouse_controller import (
    scroll_vertical
)

from server.config import (
    SCROLL_SENSITIVITY
)


def process_scroll(data):

    dy = data.get("dy", 0)

    scroll_amount = int(
        -dy *
        120 *
        SCROLL_SENSITIVITY
    )


    scroll_vertical(
        scroll_amount
    )