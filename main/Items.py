import os
import cv2

class Items:

    link = "C:/Users/theerik/PycharmProjects/tft/data/items/edited"

    def get_item_list(self, color):
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

if __name__ == '__main__':
    i = Items()
    i.get_item_list(True)