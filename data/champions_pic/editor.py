import os
from PIL import Image, ImageDraw
import json


def main():

    lista = []

    # champ_data = "C:/Users/theerik/PycharmProjects/tft/data/champions.json"

    link = "C:/Users/theerik/PycharmProjects/tft/data/champions_pic/original/"
    edit = "C:/Users/theerik/PycharmProjects/tft/data/champions_pic/edited/"

    champ_dict = {}

    # with open(champ_data) as json_file:
    #     data = json.load(json_file)
    #     # print(data[0])
    #     for p in data:
    #         name = p["championId"][5:].lower()
    #         cost = p["cost"]
    #         champ_dict[name] = cost

    size = 30, 30

    # print(champ_dict)
    for image_path in os.listdir(link):
        name = image_path[5:]
        image = Image.open(f"{link}{image_path}")
        image = image.convert("RGB")
        image.thumbnail(size, Image.ANTIALIAS)
        # (left, upper, right, lower)
        # nr = int(name[:-4])
        # if nr > 1000:
        #     # image
        #     draw = ImageDraw.Draw(image)
        #     draw.rectangle((0,0, 24,24), outline=(0,199,123))
        #     draw.rectangle((1, 1, 23, 23), outline=(0, 136, 88))
        # image = image.crop((2, 2, 22, 22))
        # if name == "25.png":
        #     image = image.crop((0, 0, 20, 15))
        #     print("a")
        # if name == "1036.png":
        #     image = image.crop((0, 0, 20, 15))
        #     print("a")
        image.save(f"{edit}{name.lower()}", "PNG")
        # break
    return lista
    pass



if __name__ == '__main__':
    main()