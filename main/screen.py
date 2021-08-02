import mss
import mss.tools
import numpy as np
import cv2
from cv2 import dnn
import time
from Templates import Templates
from Control import Control
from Champions import Champions
from static_data import Static
from Trait_to_champion import Calculator
# from Items import Items
from predict_best_comp import Predict
from path_manager import Path

class Screen:
    def __init__(self, control):

        self.color = True

        self.s = Static()
        self.control = control
        p = Path()


        # self.c = Calculator(self.s)

        self.sct = mss.mss()
        self.champs = {}
        self.items = {}
        t = Templates(p.path_templates)
        self.load_templates(t.get_badge_templates(self.color))
        c = Champions(p.path_champions)
        self.load_champions(c.get_champion_list(False))
        # i = Items()
        # self.load_items(i.get_item_list(self.color))
        self.p = Predict(self.s)

        # read model
        self.net = cv2.dnn.readNet(p.path_weights, p.path_cfg)
        # activate cuda
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
        with open(p.path_classes, "r") as f:
            self.classes = f.read().splitlines()
        self.cold_start()

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

    # def load_items(self, items: list):
    #     for i in items:
    #         name = i[0]
    #         array = i[1]
    #         self.items[name] = array
    #     pass

    def take_picture(self, monitor, color):
        if color:
            return cv2.cvtColor(np.array(self.sct.grab(monitor)), cv2.COLOR_RGBA2RGB)
        else:
            return cv2.cvtColor(np.array(self.sct.grab(monitor)), cv2.COLOR_RGBA2GRAY)




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
        lista = []
        for champ_set in champions_coords:
            name = champ_set[0]
            if name in self.s.item_to_id:
                lista.append(self.s.item_to_id[name])
                continue
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
            if name in dicta:
                dicta[name] += value
            else:
                dicta[name] = value
        return dicta, lista

    def cold_start(self):
        # prevent cold start
        test_img = self.take_picture({"top": 790, "left": 320, "width": 831, "height": 45}, self.color)
        blob = dnn.blobFromImage(test_img, 1 / 255, (416, 416), (0, 0, 0), swapRB=True, crop=False)
        self.net.setInput(blob)
        output_layers_names = self.net.getUnconnectedOutLayersNames()
        self.net.forward(output_layers_names)

    def cather_data(self, store=False, show=False):
        store_champ_monitor = {"top": 790, "left": 320, "width": 831, "height": 45}
        me = False
        acc = 0.01

        # get champs from store
        # if cant get data from store that means its other player
        store_picture = self.take_picture(store_champ_monitor, False)
        champions_in_store = self.match_champ(store_picture)

        if len(champions_in_store) > 0:
            me = True
        if me:
            count_champ_monitor = {"top": 230, "left": 135, "width": 990, "height": 450}
        else:
            count_champ_monitor = {"top": 25, "left": 355, "width": 820, "height": 315}

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
            font = cv2.FONT_HERSHEY_SIMPLEX
            colors = np.random.uniform(0, 255, size=(len(boxes), 3))

        champions_coords = []
        if len(indexes) > 0:
            for i in indexes.flatten():
                label = str(self.classes[class_ids[i]])
                x, y, w, h = boxes[i]
                champions_coords.append((label, x, y))
                # show boxes
                if show:
                    confidence = str(int(confs[i] * 100))
                    color = colors[i]
                    text = f"{label} {confidence}%"
                    cv2.rectangle(half_img, (x, y), (x + w, y + h), color, 2)
                    (ww, hh), _ = cv2.getTextSize(text, font, 0.4, 1)
                    cv2.rectangle(half_img, (x, y), (x + ww, y + 11), color, -1)
                    cv2.putText(half_img, text, (x, y + 9),
                                      font, 0.4, (255,255,255), 1)

                    # cv2.putText(half_img, (x + 2, y + 12), font, 1, color, 1)

        # show badge locations
        if show:
            for coord in badge_coords:
                x = coord[1]
                y = coord[2]
                cv2.rectangle(half_img, (x - 10, y - 10), (x, y), (255, 255, 255), 1)

        # # create champ dict
        champ_dict, item_list = self.get_tier_dict(champions_coords, badge_coords)

        # add champs from store
        if store:
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
        return me, champ_dict, item_list


    def main(self, store=False, only_me=False, show=False):

        my_number = None
        my_champ_dict = None
        my_items = None

        start_x = 1400
        start_y = 170
        shift = 63

        full_dict = {}

        total_time = time.time()
        if only_me:
            me, champ_dict, item_list = self.cather_data(store=store, show=show)
            if me:
                my_champ_dict = champ_dict
                my_items = item_list
            else:
                my_champ_dict = {}
                my_items = []
        else:
            # get data about all players
            n = 0
            for player_number in range(8):
                # for fps
                last_time = time.time()

                # move to place
                self.control.click_on_champ(start_x, start_y + shift * player_number)

                # get champions
                me, champ_dict, item_list = self.cather_data(store=store)
                if me:
                    my_number = player_number
                    my_champ_dict = champ_dict
                    my_items = item_list
                else:
                    n += 1
                    full_dict[n] = (champ_dict, item_list)
                # print("time:", time.time() - last_time)
            # go back to me
            self.control.click_on_champ(start_x, start_y + shift * my_number)
        # print("time:", time.time() - total_time)
        full_dict["me"] = (my_champ_dict, my_items)
        return full_dict


if __name__ == '__main__':
    #
    # mss.mss().shot(output="traits8.png")
    # time.sleep(1)
    c = Control()
    s = Screen(c)
    while True:
        last_time = time.time()
        # s.cather_data(True)
        me, champ_dict, item_list = s.cather_data(True)
        print(me, champ_dict, item_list)
        print("fps:", 1 / (time.time() - last_time))
        print("time:", time.time() - last_time)
        time.sleep(0.01)
    # s.main_reader(False, c)
    # s.main(c)