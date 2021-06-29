import os
import cv2

class Templates:
    def __init__(self, link):
        self.link = link

    def get_badge_templates(self):
        """
        1st value is bronze, 2nd silver and 3rd gold
        :return:
        """
        lista = []
        badge_link = self.link + "/pictures/badges"
        for image_path in os.listdir(badge_link):
            # create the full input path and read the file
            input_path = os.path.join(badge_link, image_path)
            array = cv2.imread(input_path)
            lista.append(array)
        return lista
