import os
import cv2

class Champions:
    def __init__(self, link):
        self.link = link
        pass

    def get_champion_list(self):
        lista = []
        badge_link = self.link + "/pictures/champions/edited"
        for image_path in os.listdir(badge_link):
            # create the full input path and read the file
            name = image_path[:-4].lower()
            input_path = os.path.join(badge_link, image_path)
            array = cv2.imread(input_path, 0)
            lista.append((name, array))
        return lista

if __name__ == '__main__':
    c = Champions("pictures/set5/champions.json")
    c.load()
