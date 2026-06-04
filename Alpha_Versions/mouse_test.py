import time

from phase_5A.server.mouse_controller import (
    move_mouse_relative
)


print("Starting in 3 seconds...")

time.sleep(3)


move_mouse_relative(200, 0)

print("Done.")