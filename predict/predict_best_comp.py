from static_data import Static, item_to_parts

class Predict:
    def __init__(self):
        s = Static()
        s.read("C:/Users/theerik/PycharmProjects/tft/data/champions.json")
        s.read_items("C:/Users/theerik/PycharmProjects/tft/data/items.json")
        s.read_traits("C:/Users/theerik/PycharmProjects/tft/data/traits.json")
        s.read_comps_tftactics("C:/Users/theerik/PycharmProjects/tft/data/comps_tactics.json")
        self.s = s
        self.comps = s.comps
        self.champion_to_traits = s.champion_to_traits
        self.trait_to_champions = s.trait_to_champions
        # self.link_to_csv = link_to_csv

    def get_item_parts(self, item):
        pass

    def predict_main(self, champions, items):
        """
        :param champions: champion ids
        :param items: item ids
        :return:
        """
        top5 = []
        seta = set(champions)
        if 0 in seta:
            seta.remove(0)
        size = len(seta)
        size_i = len(items)
        for key in self.comps:
            comp_dict = self.comps[key]
            if len(comp_dict) == 1:
                continue
            core_champs = comp_dict["needed_champs"]
            start_champs = comp_dict["early_champs"]
            extra_champs = comp_dict["extra_champs"]

            core_items = comp_dict["needed_items"]
            core_parts = comp_dict["needed_parts"]
            # core_parts_size = comp_dict["needed_parts_size"]
            core_parts_size = len(core_items) * 2

            extra_items = comp_dict["extra_items"]
            extra_parts = comp_dict["extra_parts"]
            # extra_parts_size = comp_dict["extra_parts_size"]
            extra_parts_size = len(extra_items) * 2

            high = len(seta.intersection(core_champs))
            med = len(seta.intersection(extra_champs))
            low = len(seta.intersection(start_champs))

            # print(items)
            # print(core_items)
            # print(core_parts)
            # print(core_parts_size)
            # print(extra_items)
            # print(extra_parts)
            # print(extra_parts_size)
            # print("----")

            high_i = 0
            high_p = 0
            low_i = 0
            low_p = 0
            # first check items and then parts so
            # it would not double count
            for item in items:
                # item
                if item % 1000 >= 10:
                    if item in core_items:
                        core_items.remove(item)
                        some_list = []
                        item_to_parts(item, some_list)
                        for part in some_list:
                            core_parts.remove(part)

                        high_i += 1
                    elif item in extra_items:
                        extra_items.remove(item)
                        low_i += 1
                        some_list = []
                        item_to_parts(item, some_list)
                        for part in some_list:
                            extra_parts.remove(part)

            for item in items:
                # part
                if item % 1000 < 10:
                    if item in core_parts:
                        core_parts.remove(item)
                        high_p += 1
                    elif item in extra_parts:
                        extra_parts.remove(item)
                        low_p += 1

            # print(core_items)
            # print(core_parts)
            # print(core_parts_size)
            # print(extra_items)
            # print(extra_parts)
            # print(extra_parts_size)
            # print("champs", high, med, low)
            # print("items", high_i, high_p, low_i, low_p)

            # calculate the final score for sort
            # change here
            # champs
            score1 = high / size + \
                    0.8 * low / (size + len(start_champs)) + \
                    0.7 * med / (size + len(extra_champs))
            # items
            score2 = high_i / size_i + \
                     0.7 * (low_i / size_i) + \
                     0.7 * high_p / (2 * size_i) + \
                     0.5 * (low_p / (2 * size_i))

            score = score1 + 0.75 * score2
            top5.append((round(score, 3), key, high, med, low, size,
                         high_i, high_p, low_i, low_p, size_i))
            top5.sort(key=lambda x: x[0], reverse=True)
            if len(top5) > 5:
                del top5[5]

            # info
            # print(key, comp_dict["name"])
        return top5


if __name__ == '__main__':
    p = Predict()
    # p.s.number_to_names(
    #     (19, 9, 55, 24)
    # )
    # print(p.s.id_to_item[99])
    # print(p.s.id_to_item[9])
    # print(p.s.id_to_item[1])
    top5 = p.predict_main(
        (19, 9, 55, 24, 14, 1),
        (14, 1,2,3,4)
    )
    print("  scr key hg md lw sz hi hp li lp si")
    print(top5[0])
    print(top5[1])
    print(top5[2])
    print(top5[3])
    print(top5[4])
