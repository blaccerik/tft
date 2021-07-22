import os
# import cv2
import PIL

class Champions_pic:

    link = "C:/Users/theerik/PycharmProjects/tft/data/champions_pic/edited"

    def get_champion_list(self):
        lista = []

        for image_path in os.listdir(self.link):
            # create the full input path and read the file
            name = image_path[:-4].lower()
            input_path = os.path.join(self.link, image_path)
            array = PIL.Image.open(input_path)
            # array = cv2.imread(input_path, cv2.IMREAD_COLOR)
            lista.append((name, array))
        return lista