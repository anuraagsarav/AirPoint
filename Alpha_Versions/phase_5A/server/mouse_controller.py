import pyautogui

pyautogui.FAILSAFE = False


def move_mouse_relative(dx, dy):

    print("MOVE FUNCTION CALLED")

    print(f"dx={dx}, dy={dy}")

    pyautogui.moveRel(dx, dy)

    print("MOVE COMPLETED")