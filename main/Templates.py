import os
import cv2

class Templates:

    def __init__(self, link):
        self.link = link

    def get_badge_templates(self, color):
        """
        1st value is bronze, 2nd silver and 3rd gold
        :return:
        """
        if color:
            x = cv2.IMREAD_COLOR
        else:
            x = cv2.IMREAD_GRAYSCALE

        lista = []
        for image_path in os.listdir(self.link):
            # create the full input path and read the file
            input_path = os.path.join(self.link, image_path)
            array = cv2.imread(input_path, x)
            lista.append(array)
        return lista
