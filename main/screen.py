import mss
import mss.tools
import numpy as np
import cv2
import time
import difflib
from pytesseract import pytesseract
from Templates import Templates
from Control import Control
from Champions import Champions
from static_data import Static
from Trait_to_champion import Calculator

class Screen:
    def __init__(self):

        self.color = False

        self.s = Static()

        self.c = Calculator(self.s)

        self.sct = mss.mss()
        self.champs = {}
        t = Templates()
        self.load_templates(t.get_badge_templates(self.color))
        c = Champions()
        self.load_champions(c.get_champion_list(self.color))

    def load_templates(self, templates: list):
        self.bronze = templates[0]
        self.silver = templates[1]

    def load_champions(self, champions: list):
        for i in champions:
            name = i[0]
            array = i[1]
            self.champs[name] = array
        pass

    def take_picture(self, monitor, color):
        if color:
            return cv2.cvtColor(np.array(self.sct.grab(monitor)), cv2.COLOR_RGBA2RGB)
        else:
            return cv2.cvtColor(np.array(self.sct.grab(monitor)), cv2.COLOR_RGBA2GRAY)
    #
    # def modify_picture(self, picture):
    #     return self.read_picture(picture)

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
        res = cv2.matchTemplate(image, smaller_image, method)
        loc = np.where(res >= threshold)

        coords = []

        # color issue
        if self.color:
            w, h, nr = smaller_image.shape
        else:
            w, h = smaller_image.shape

        for pt in zip(*loc[::-1]):
            x = pt[0]
            y = pt[1]
            cv2.rectangle(image, pt, (x + w, y + h), (255, 255, 255), 2)
            coords.append((x,y))
            count += 1
        return count

    # def find_champions(self, image):
    #     # ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
    #     # 'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']
    #     method = cv2.TM_SQDIFF_NORMED
    #     for name in self.champs:
    #         # print(self.champs.keys())
    #         template = self.champs[name]
    #         # print(template.shape[:-1])
    #         w, h = template.shape[:-1]
    #
    #         # print(image)
    #         res = cv2.matchTemplate(image, template, method)
    #         min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    #         if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
    #             top_left = min_loc
    #         else:
    #             top_left = max_loc
    #
    #         bottom_right = (top_left[0] + w, top_left[1] + h)
    #         # print(name, mn)
    #
    #         # print(name, min_val, max_val, min_loc, max_loc)
    #
    #         if min_val < 0.15:
    #             print(name, min_val)
    #             cv2.rectangle(image, top_left, bottom_right, (255,255,255), 2)
    #
    #         # if mn < 0.14:
    #         #     print(name, mn)
    #         #     # Draw the rectangle:
    #         #     # Extract the coordinates of our best match
    #         #     MPx, MPy = mnLoc
    #         #
    #         #     # Step 2: Get the size of the template. This is the same size as the match.
    #         #     trows, tcols = template.shape[:2]
    #         #
    #         #     # Step 3: Draw the rectangle on large_image
    #         #     cv2.rectangle(image, (MPx, MPy), (MPx + tcols, MPy + trows), (255, 255, 255), 2)
    #
    #
    #     # Display the original image with the rectangle around the match.
    #     cv2.imshow('output', image)
    #
    #     # Press "q" to quit
    #     if cv2.waitKey(25) & 0xFF == ord("q"):
    #         cv2.destroyAllWindows()
    #     # print(res)
    #     pass

    def text_to_trait(self, text):
        text = text.lower()
        if text in self.s.trait_to_champions:
            return text
        else:
            some = difflib.get_close_matches(text, self.s.trait_to_champions)
            if len(some) > 0:
                return some[0]

    def text_to_number(self, text):
        if len(text) > 0:
            nr = int(text[0])
            return nr

    def main_reader(self, me: bool, control: Control):

        if me:
            count_champ_monitor = {"top": 0, "left": 0, "width": 1440, "height": 900}
        else:
            count_champ_monitor = {"top": 68, "left": 355, "width": 722, "height": 271}
        method = cv2.TM_CCOEFF_NORMED
        badge_threshold = 0.7
        what_traits_monitor = {"top": 239, "left": 43, "width": 103, "height": 434}
        count_traits_monitor = {"top": 239, "left": 9, "width": 1, "height": 450}
        count_traits_monitor_edit = {"top": 239, "left": 9, "width": 150, "height": 450}
        strip_length = 33

        while True:
            # for fps
            last_time = time.time()
            half_img = self.take_picture(count_champ_monitor, self.color)

            count = 0

            dicta = {}

            # find all silver champs on screen
            count = self.make_match(half_img, self.silver, method, badge_threshold, count)
            # find all bronze champs on screen
            count = self.make_match(half_img, self.bronze, method, badge_threshold, count)
            # todo gold champs

            # find number of active/unactive traits
            shift = 0
            count_completed = 0
            count_uncompleted = 0

            # # only needs number of champions and th traits
            # here calculate the champions when given the traits

            # cv2.imshow("half image", left_image)
            # if cv2.waitKey(25) & 0xFF == ord("q"):
            #     cv2.destroyAllWindows()
            #     break

            strip_original = self.take_picture(count_traits_monitor, self.color)
            b = self.take_picture(count_traits_monitor_edit, self.color)

            shift = 0
            count_completed = 0
            count_uncompleted = 0
            # count active traits
            for i in range(10):
                add = i * 42
                # b = a[add:add + strip_length, :, :]

                # only let "right" traits through
                strip_edit = strip_original[add:add + strip_length]
                average = np.average(strip_edit)
                if average <= 40:
                    shift = add
                    break

                # increase contrast
                bb = b[add:add + strip_length]
                # Get brightness range - i.e. darkest and lightest pixels
                minv = np.min(bb)  # result=144
                maxv = np.max(bb)  # result=216

                # Make a LUT (Look-Up Table) to translate image values
                LUT = np.zeros(256, dtype=np.uint8)
                LUT[minv:maxv + 1] = np.linspace(start=0, stop=255, num=(maxv - minv) + 1, endpoint=True, dtype=np.uint8)

                bb = LUT[bb]

                # find the number in front of the trait
                number_part = bb[:, 35:52]
                text = pytesseract.image_to_string(number_part, config='--psm 10 -c tessedit_char_whitelist=0123456789')
                nr = self.text_to_number(max(text.splitlines()))

                # find trait word
                word_part = bb[0:17, 58:150]
                text = pytesseract.image_to_string(word_part, config='--psm 8 -c tessedit_char_whitelist='
                                                                       'aAbBcCdDeEfFgGhHiIkKlLmMnNoOpPrRsStTuUvVwWyY')
                text = self.text_to_trait(max(text.splitlines()))
                count_completed += 1

                dicta[text] = nr


            # count unactive traits
            # might be wrong
            if shift != 0:
                shift += 20
            for i in range(10 - count_completed):
                add = i * 42
                strip_edit = strip_original[add + shift:add + shift + strip_length]
                average = np.average(strip_edit)
                if average > 40:
                    # shift = add
                    break

                bb = b[add + shift:add + shift + strip_length]

                # Get brightness range - i.e. darkest and lightest pixels
                minv = np.min(bb)  # result=144
                maxv = np.max(bb)  # result=216

                # Make a LUT (Look-Up Table) to translate image values
                LUT = np.zeros(256, dtype=np.uint8)
                LUT[minv:maxv + 1] = np.linspace(start=0, stop=255, num=(maxv - minv) + 1, endpoint=True, dtype=np.uint8)

                bb = LUT[bb]

                # cv2.imshow("a", number_part)
                # if cv2.waitKey(25) & 0xFF == ord("q"):
                #     cv2.destroyAllWindows()
                #     break
                # time.sleep(1)

                # find trait word
                word_part = bb[0:18, 38:130]
                text = pytesseract.image_to_string(word_part, config='--psm 8 -c tessedit_char_whitelist='
                                                                     'aAbBcCdDeEfFgGhHiIkKlLmMnNoOpPrRsStTuUvVwWyY')
                trait = self.text_to_trait(max(text.splitlines()))

                if min(self.s.trait_to_sets[trait]) == 2:
                    nr = 1
                else:
                    # find the number in front of the trait
                    number_part = bb[17:42, 38:52]

                    text = pytesseract.image_to_string(number_part,
                                                       config='--psm 10 -c tessedit_char_whitelist=12')
                    nr = self.text_to_number(max(text.splitlines()))

                count_uncompleted += 1

                dicta[trait] = nr
            if count > 0:
                print(count, dicta)
                final_list = self.c.main(dicta, count)
                print(final_list)
            # cv2.imshow("hi", aa)
            # cv2.imshow("b", b)
            # if cv2.waitKey(25) & 0xFF == ord("q"):
            #     cv2.destroyAllWindows()
            #     break
            print("time:", time.time() - last_time)
            time.sleep(0.01)
        pass


if __name__ == '__main__':
    #
    # mss.mss().shot(output="traits8.png")
    s = Screen()
    c = Control()
    s.main_reader(False, c)