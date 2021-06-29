import pyautogui
import time

class Control:

    def __init__(self):
        pass

    def move(self, x, y):
        pyautogui.moveTo(x,y)
