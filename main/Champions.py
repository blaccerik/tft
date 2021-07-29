import os
import cv2

class Champions:

    def __init__(self, link):
        self.link = link

    def get_champion_list(self, color):
        lista = []

        if color:
            x = cv2.IMREAD_COLOR
        else:
            x = cv2.IMREAD_GRAYSCALE

        for image_path in os.listdir(self.link):
            # create the full input path and read the file
            name = image_path[:-4].lower()
            input_path = os.path.join(self.link, image_path)
            array = cv2.imread(input_path, x)
            lista.append((name, array))
        return lista
