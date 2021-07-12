import pyautogui
import time

class Control:

    def __init__(self):
        pass

    def move(self, x, y):
        pyautogui.moveTo(x,y)

    def click_on_champ(self, x, y):
        pyautogui.mouseDown(x=x, y=y, button='left')
        time.sleep(0.001)
        pyautogui.mouseUp(button='left')
