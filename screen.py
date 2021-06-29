import mss
import mss.tools
from PIL import Image
import numpy as np
import pyautogui
import cv2
import time
from Templates import Templates
from ChampionList import ChampionList
from Control import Control
import pytesseract
from pytesseract import Output
from Champions import Champions

class Screen:
    def __init__(self):
        self.sct = mss.mss()
        self.bronze = None
        self.silver = None
        self.champs = {}
        pass

    def load_templates(self, templates: list):
        self.bronze = templates[0]
        self.silver = templates[1]

    def load_champions(self, champions: list):
        for i in champions:
            name = i[0]
            array = i[1]
            self.champs[name] = array
        pass

    def take_picture(self, monitor, color=True):
        if color:
            return cv2.cvtColor(np.array(self.sct.grab(monitor)), cv2.COLOR_RGBA2RGB)
        else:
            return cv2.cvtColor(np.array(self.sct.grab(monitor)), cv2.COLOR_RGBA2GRAY)

    def modify_picture(self, picture):
        return self.read_picture(picture)

    def read_picture(self, picture):
        # how many traits
        # click on all the traits and see what champions on the field

        # read store

        # read gold
        pass

    def read_traits(self):
        pass

    def read_champions(self):
        pass

    def read_store(self):
        pass

    def make_match(self, image, smaller_image, method, threshold, count):

        # todo make sure same place is not counted twice
        coords = []
        res = cv2.matchTemplate(image, smaller_image, method)
        loc = np.where(res >= threshold)
        w, h = smaller_image.shape[:-1]
        for pt in zip(*loc[::-1]):
            x = pt[0]
            y = pt[1]
            cv2.rectangle(image, pt, (x + w, y + h), (255, 255, 255), 2)
            coords.append((x,y))
            count += 1
        return image, count



    def find_champions(self, image):
        # ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
        # 'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']
        method = cv2.TM_SQDIFF_NORMED
        for name in self.champs:
            # print(self.champs.keys())
            template = self.champs[name]
            # print(template.shape[:-1])
            w, h = template.shape

            # print(image)
            res = cv2.matchTemplate(image, template, method)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
                top_left = min_loc
            else:
                top_left = max_loc

            bottom_right = (top_left[0] + w, top_left[1] + h)
            # print(name, mn)

            # print(name, min_val, max_val, min_loc, max_loc)

            if min_val < 0.1:
                print(name, min_val)
                cv2.rectangle(image, top_left, bottom_right, (255,255,255), 2)

            # if mn < 0.14:
            #     print(name, mn)
            #     # Draw the rectangle:
            #     # Extract the coordinates of our best match
            #     MPx, MPy = mnLoc
            #
            #     # Step 2: Get the size of the template. This is the same size as the match.
            #     trows, tcols = template.shape[:2]
            #
            #     # Step 3: Draw the rectangle on large_image
            #     cv2.rectangle(image, (MPx, MPy), (MPx + tcols, MPy + trows), (255, 255, 255), 2)


        # Display the original image with the rectangle around the match.
        cv2.imshow('output', image)

        # Press "q" to quit
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
        # print(res)
        pass

    def main_reader(self, me: bool, control: Control):

        if me:
            count_champ_monitor = {"top": 0, "left": 0, "width": 1440, "height": 900}
        else:
            count_champ_monitor = {"top": 68, "left": 355, "width": 722, "height": 271}
        method = cv2.TM_CCOEFF_NORMED
        badge_threshold = 0.7
        count_traits_monitor = {"top": 247, "left": 9, "width": 1, "height": 450}
        strip_length = 13

        champion_monitor = {"top": 350, "left": 135, "width": 160, "height": 320}
        while True:

            last_time = time.time()

            # array = self.take_picture(count_champ_monitor)
            # half_img = array
            # count = 0
            # # find all silver champs on screen
            # half_img, count = self.make_match(half_img, self.silver, method, badge_threshold, count)
            # # find all bronze champs on screen
            # half_img, count = self.make_match(half_img, self.bronze, method, badge_threshold, count)
            # # todo gold champs
            #
            # a = self.take_picture(count_traits_monitor)
            # print("total", count)
            # champ_list = ChampionList(count)
            #
            # shift = 0
            # count_completed = 0
            # count_uncompleted = 0
            # # count active traits
            # for i in range(10):
            #     add = i * 43
            #     # b = a[add:add + strip_length, :, :]
            #     c = a[add:add + strip_length, :, :]
            #     # if cv2.waitKey(25) & 0xFF == ord("q"):
            #     #     cv2.destroyAllWindows()
            #     #     break
            #     average = np.average(c)
            #     # print(average)
            #     if average <= 30:
            #         shift = add
            #         break
            #     # cv2.imshow("a", b)
            #     count_completed += 1
            #     # time.sleep(0.1)
            #
            # for i in range(count_completed):
            #     add = i * 43
            #     control.move(20, 250 + add)
            #     self.take_picture(champion_monitor, color=False)
            #     # todo take picture of the champs in traits
            #     # add them to champ list
            #     time.sleep(0.5)
            #
            #
            # # count unactive traits
            # # might be wrong
            # if shift != 0:
            #     shift += 18
            # for i in range(10 - count_completed):
            #     add = i * 43
            #     # b = a[add + shift:add + shift + strip_length, :, :]
            #     c = a[add + shift:add + shift + strip_length, :, :]
            #     # if cv2.waitKey(25) & 0xFF == ord("q"):
            #     #     cv2.destroyAllWindows()
            #     #     break
            #     average = np.average(c)
            #     # print(average)
            #     if average > 40:
            #         # shift = add
            #         break
            #     # cv2.imshow("a", b)
            #     count_uncompleted += 1
            #     # time.sleep(0.1)
            # for i in range(count_uncompleted):
            #     add = i * 43
            #     control.move(20, 250 + shift + add)
            #     time.sleep(0.5)
            # print("traits", count_completed, count_uncompleted)
            # aa = self.take_picture(champion_monitor, color=False)
            self.find_champions(self.take_picture(champion_monitor, color=False))
            # cv2.imshow("hi", aa)
            # if cv2.waitKey(25) & 0xFF == ord("q"):
            #     cv2.destroyAllWindows()
            #     break
            print("fps: {}".format(1 / (time.time() - last_time)))
            time.sleep(1)
        pass


if __name__ == '__main__':
    # time.sleep(5)
    #
    # mss.mss().shot(output="traits8.png")

    print("aaa")

    s = Screen()
    t = Templates("C:/Users/theerik/PycharmProjects/tft")
    champs = Champions("C:/Users/theerik/PycharmProjects/tft")

    s.load_templates(t.get_badge_templates())
    s.load_champions(champs.get_champion_list())

    c = Control()

    s.main_reader(False, c)

    # n = 100
    # while n > 0:
    #     n -= 1
    #     print(pyautogui.position())
    #     time.sleep(1)