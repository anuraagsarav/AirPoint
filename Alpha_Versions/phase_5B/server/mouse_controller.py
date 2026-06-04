import pyautogui


pyautogui.FAILSAFE = False


def move_mouse_relative(dx, dy):

    #print(f"MOVE FUNCTION | dx={dx} dy={dy}")

    pyautogui.moveRel(dx, dy)


def left_click():

    #print("LEFT CLICK FUNCTION")

    pyautogui.mouseDown()

    pyautogui.mouseUp()


def right_click():

    #print("RIGHT CLICK FUNCTION")

    pyautogui.click(button="right")