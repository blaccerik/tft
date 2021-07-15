import mss
import mss.tools
import numpy as np
import cv2
from cv2 import dnn
import time
import difflib

from PIL import Image
from pytesseract import pytesseract
from Templates import Templates
from Control import Control
from Champions import Champions
from static_data import Static
from Trait_to_champion import Calculator
from Items import Items
from predict_best_comp import Predict, same_length

class Screen:
    def __init__(self):

        self.color = True

        self.s = Static()

        self.c = Calculator(self.s)

        self.sct = mss.mss()
        self.champs = {}
        self.items = {}
        t = Templates()
        self.load_templates(t.get_badge_templates(self.color))
        c = Champions()
        self.load_champions(c.get_champion_list(False))
        i = Items()
        self.load_items(i.get_item_list(self.color))
        self.p = Predict(self.s)


        weights = "C:/Users/theerik/PycharmProjects/tft/data/images/network/yolov3_training_last.weights"
        cfg = "C:/Users/theerik/PycharmProjects/tft/data/images/network/yolov3_testing.cfg"
        classes_link = "C:/Users/theerik/PycharmProjects/tft/data/images/network/classes.txt"
        # read model
        self.net = cv2.dnn.readNet(weights, cfg)
        # activate cuda
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

        with open(classes_link, "r") as f:
            self.classes = f.read().splitlines()

    def load_templates(self, templates: list):
        self.bronze = templates[0]
        self.silver = templates[1]
        # 0 is bronze, 1 gold, 2 silver
        self.badges = templates

    def load_champions(self, champions: list):
        for i in champions:
            name = i[0]
            array = i[1]
            self.champs[name] = array
        pass

    def load_items(self, items: list):
        for i in items:
            name = i[0]
            array = i[1]
            self.items[name] = array
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















    def are_same(self, image, image2):
        # todo make sure same place is not counted twice
        if image2 is None:
            return True

        res = cv2.matchTemplate(image, image2, cv2.TM_SQDIFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if min_val < 0.1:
            return False
        # for pt in zip(*loc[::-1]):
        #     print(res)
        #     return True
        # return False
        return True

    def match_badge(self, image, badge_id, coords):

        shift_x = 10
        shift_y = 10

        method = cv2.TM_CCOEFF_NORMED
        threshold = 0.75
        smaller_img = self.badges[badge_id]
        res = cv2.matchTemplate(image, smaller_img, method)
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):
            x = pt[0]
            y = pt[1]
            if badge_id == 2:
                x += 6
            if badge_id == 1:
                x += 9
            coords.append((badge_id, x+ shift_x, y + shift_y))


    def match_champ(self, image):
        method = cv2.TM_CCOEFF_NORMED
        threshold = 0.95
        lista = []
        for key in self.champs:
            array = self.champs[key]
            res = cv2.matchTemplate(image, array, method)
            loc = np.where(res >= threshold)
            for pt in zip(*loc[::-1]):
                # x = pt[0]
                # y = pt[1]
                # print(key)
                lista.append(key)
        return lista

    def get_tier_dict(self, champions_coords, badge_coords):
        """
        Match champions and their tiers
        closest one to the radius center is the final one
        :param champions_coords:
        :param badge_coords:
        :return:
        """
        radius = 50
        dicta = {}
        for champ_set in champions_coords:
            champ_name = champ_set[0]
            champ_x = champ_set[1]
            champ_y = champ_set[2]
            best = 0
            best_index = None
            best_error = 2 * radius + 1
            for badge_set_index in range(len(badge_coords)):
                badge_set = badge_coords[badge_set_index]
                badge_id = badge_set[0]
                badge_x = badge_set[1]
                badge_y = badge_set[2]
                xx = abs(champ_x - badge_x)
                yy = abs(champ_y - badge_y)
                if xx < radius and yy < radius and xx + yy < best_error:
                    best_error = xx + yy
                    best = badge_id
                    best_index = badge_set_index
            if best_index is not None:
                del badge_coords[best_index]
            if best == 0:
                value = 1
            elif best == 2:
                value = 3
            else:
                value = 9
            if champ_name in dicta:
                dicta[champ_name] += value
            else:
                dicta[champ_name] = value
        return dicta

    def cather_data(self, show=False):
        store_champ_monitor = {"top": 790, "left": 320, "width": 831, "height": 45}
        me = False
        acc = 0.10

        # get champs from store
        # if cant get data from store that means its other player
        store = self.take_picture(store_champ_monitor, False)
        champions_in_store = self.match_champ(store)

        if len(champions_in_store) > 0:
            me = True
        if me:
            count_champ_monitor = {"top": 230, "left": 210, "width": 900, "height": 450}
        else:
            count_champ_monitor = {"top": 25, "left": 355, "width": 690, "height": 315}

        # take picture of the champions
        half_img = self.take_picture(count_champ_monitor, self.color)

        # # find number of champs
        badge_coords = []
        self.match_badge(half_img, 0, badge_coords)
        self.match_badge(half_img, 2, badge_coords)
        self.match_badge(half_img, 1, badge_coords)

        # take picture with yolo
        height, width, _ = half_img.shape
        # 416 is default size, do not change
        blob = dnn.blobFromImage(half_img, 1 / 255, (416, 416), (0, 0, 0), swapRB=True, crop=False)
        self.net.setInput(blob)
        output_layers_names = self.net.getUnconnectedOutLayersNames()
        # print(output_layers_names)
        layerOutputs = self.net.forward(output_layers_names)
        boxes = []
        confs = []
        class_ids = []
        # detect
        for output in layerOutputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                conf = scores[class_id]
                if conf > acc:
                    cenx = int(detection[0] * width)
                    ceny = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = int(cenx - w / 2)
                    y = int(ceny - h / 2)
                    boxes.append([x, y, w, h])
                    confs.append((float(conf)))
                    class_ids.append(class_id)

        # 0.4 default
        # sometimes error
        indexes = dnn.NMSBoxes(boxes, confs, acc, 0.4)

        # for boxes
        if show:
            font = cv2.FONT_HERSHEY_PLAIN
            colors = np.random.uniform(0, 255, size=(len(boxes), 3))

        champions_coords = []
        if len(indexes) > 0:
            for i in indexes.flatten():
                label = str(self.classes[class_ids[i]])
                x, y, w, h = boxes[i]
                champions_coords.append((label, x, y))
                # show boxes
                if show:
                    confidence = str(round(confs[i], 2))
                    color = colors[i]
                    cv2.rectangle(half_img, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(half_img, label + " " + confidence, (x, y + 20), font, 2, (255, 255, 255), 2)

        # show badge locations
        if show:
            for coord in badge_coords:
                x = coord[1]
                y = coord[2]
                cv2.rectangle(half_img, (x, y), (x + 60, y + 60), (255, 255, 255), 1)

        # create champ dict
        champ_dict = self.get_tier_dict(champions_coords, badge_coords)

        # add champs from store
        for champ in champions_in_store:
            if champ in champ_dict:
                champ_dict[champ] += 1
            else:
                champ_dict[champ] = 1
        if show:
            cv2.imshow("b", half_img)
            if cv2.waitKey(25) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                return
        return me, champ_dict


    def main(self, control):
        my_number = None
        start_x = 1400
        start_y = 170
        shift = 63

        # # prevent cold start
        # test_img = self.take_picture({"top": 790, "left": 320, "width": 831, "height": 45}, self.color)
        # blob = dnn.blobFromImage(test_img, 1 / 255, (416, 416), (0, 0, 0), swapRB=True, crop=False)
        # self.net.setInput(blob)
        # output_layers_names = self.net.getUnconnectedOutLayersNames()
        # self.net.forward(output_layers_names)

        total_time = time.time()
        # get data about all players
        for player_number in range(8):
            # for fps
            last_time = time.time()

            # move to place
            control.click_on_champ(start_x, start_y + shift * player_number)

            # todo check if player is alive

            # get champions
            me, champ_dict = self.cather_data()
            if me:
                my_number = player_number

            # predict
            top5 = self.p.predict_main(champ_dict, [], 5)
            same_length(top5)
            print("time:", time.time() - last_time)
        print("total time:", time.time() - total_time)
        print(my_number)
        pass


if __name__ == '__main__':
    #
    # mss.mss().shot(output="traits8.png")
    time.sleep(1)
    s = Screen()
    c = Control()
    # s.main_reader(False, c)
    s.main(c)