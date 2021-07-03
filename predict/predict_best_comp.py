from static_data import Static, item_to_parts

class Predict:
    def __init__(self):
        s = Static()
        s.read("C:/Users/theerik/PycharmProjects/tft/data/champions.json")
        s.read_items("C:/Users/theerik/PycharmProjects/tft/data/items.json")
        s.read_traits("C:/Users/theerik/PycharmProjects/tft/data/traits.json")
        s.read_comps_tftactics("C:/Users/theerik/PycharmProjects/tft/data/comps_tactics.json", only_s=False)
        self.s = s
        self.comps = s.comps
        self.champion_to_traits = s.champion_to_traits
        self.trait_to_champions = s.trait_to_champions
        self.id_to_tier = s.id_to_tier
        # self.link_to_csv = link_to_csv

    def get_same_items_and_champs(self, champions: dict, items: list, comp_dict: dict):
        core_champs = comp_dict["needed_champs"]
        start_champs = comp_dict["early_champs"]
        extra_champs = comp_dict["extra_champs"]

        core_items = comp_dict["needed_items"]
        core_parts = comp_dict["needed_parts"]
        core_parts_size = len(core_items) * 2

        extra_items = comp_dict["extra_items"]
        extra_parts = comp_dict["extra_parts"]
        extra_parts_size = len(extra_items) * 2

        # keep track of the keys(champs) that were overlapping
        # use it in calculation and factor in level
        core_count = []
        start_count = []
        extra_count = []
        # does not work if champs overlap -> core = [1,2], extra = [1]
        # only one "1" will be counted and added
        # change here if needed
        for champ_key in champions:
            if champ_key in core_champs:
                core_count.append(champ_key)
            elif champ_key in start_champs:
                start_count.append(champ_key)
            elif champ_key in extra_champs:
                extra_count.append(champ_key)

        # print(items)
        # print(core_items)
        # print(core_parts)
        # print(core_parts_size)
        # print(extra_items)
        # print(extra_parts)
        # print(extra_parts_size)
        # print("----")

        core_i = 0
        core_p = 0
        extra_i = 0
        extra_p = 0
        # first check items and then parts so
        # it would not double count
        for item in items:
            # item
            if item % 1000 > 10:
                if item in core_items:
                    core_items.remove(item)
                    some_list = []
                    item_to_parts(item, some_list)
                    for part in some_list:
                        core_parts.remove(part)
                    core_i += 1
                elif item in extra_items:
                    extra_items.remove(item)
                    extra_i += 1
                    some_list = []
                    item_to_parts(item, some_list)
                    for part in some_list:
                        extra_parts.remove(part)
        for item in items:
            # part
            if item % 1000 < 10:
                if item in core_parts:
                    core_parts.remove(item)
                    core_p += 1
                elif item in extra_parts:
                    extra_parts.remove(item)
                    extra_p += 1

        return core_count, start_count, extra_count, \
               core_i, core_p, core_parts_size, \
               extra_i, extra_p, extra_parts_size

    def find_level(self, nr, id):
        """
        Does not actually find the level but the score of how many copies of that champion you have
        lvl 1 = 0.5
        lvl 2 = 1
        lvl 3 = 2
        todo add tier system -> tier 0-1 (grey, green) give x amount of score etc
        :return:
        """
        tier = self.id_to_tier[id]
        if tier < 2:
            x = 0.8
        elif tier == 3:
            x = 0.9
        else:
            x = 1.1

        if nr < 3:
            return x * 0.5
        elif nr < 6:
            return x * 1
        elif nr < 9:
            return x * 1.5
        else:
            return x * 2

    def predict_main(self, champions, items):
        """
        :param champions: champion ids [1,5,1,1,4,0]
        :param items: item ids
        :return:
        """
        top5 = []
        if 0 in champions:
            del champions[0]
        size = len(champions)
        size_i = len(items)
        for key in self.comps:
            comp_dict = self.comps[key]

            tier = comp_dict["name"][0].lower()

            if tier == "s":
                tier = 1.3
            elif tier == "a":
                tier = 1
            else:
                tier = 0.7

            if len(comp_dict) == 1:
                continue
            core_count, start_count, extra_count, \
            core_i, core_p, core_parts_size, \
            extra_i, extra_p, extra_parts_size = self.get_same_items_and_champs(champions, items, comp_dict)

            # print(core_count, start_count, extra_count)
            # print(core_i, core_p, core_parts_size)
            # print(extra_i, extra_p, extra_parts_size)

            # calculate the final score for sort
            # change here

            core_size = 0
            start_size = 0
            extra_size = 0
            for champ in core_count:
                nr = champions[champ]
                core_size += self.find_level(nr, champ)
            for champ in start_count:
                nr = champions[champ]
                start_size += self.find_level(nr, champ)
            for champ in extra_count:
                nr = champions[champ]
                extra_size += self.find_level(nr, champ)

            score1 = core_size / size + 0.8 * start_size / size + 0.7 * extra_size / size


            # score1 = high / size + \
            #         0.8 * low / (size + len(start_champs)) + \
            #         0.7 * med / (size + len(extra_champs))

            # items
            # score2 = high_i / size_i + \
            #          0.7 * (low_i / size_i) + \
            #          0.7 * high_p / (2 * size_i) + \
            #          0.5 * (low_p / (2 * size_i))
            score2 = core_i / (core_parts_size * 2) + \
                     0.8 * extra_i / (extra_parts_size * 2) + \
                     0.9 * core_p / (core_parts_size) + \
                     0.8 * extra_p / (extra_parts_size)

            score = tier * (1.0 * score1 + 1.0 * score2 + 0.001)
            top5.append((round(score, 3), key, core_size, start_size, extra_size, size,
                         core_i, core_p, extra_i, extra_p, size_i))
            top5.sort(key=lambda x: x[0], reverse=True)
            if len(top5) > 5:
                del top5[5]

            # info
            print(key, comp_dict["name"])
        return top5


if __name__ == '__main__':
    p = Predict()
    p.s.number_to_names(
        (26, 8, 44, 23, 48)
    )
    p.s.number_to_items(
        (1009, 9, 3, 5)
    )
    print(p.s.champ_to_id["tft5_teemo"])
    # print(p.s.champ_to_id["tft5_warwick"])
    # print(p.s.champ_to_id["tft5_thresh"])
    # print(p.s.id_to_item[99])
    # print(p.s.id_to_item[9])
    # print(p.s.id_to_item[1])
    top5 = p.predict_main(
        {26: 9, 8:1, 44: 3, 23: 5, 48: 1},
        (1009, 9, 3, 5, 2, 5, 1005, 1034)
    )
    print("   scr key cs ss es  s ci cp ei ep si")
    print(top5[0])
    print(top5[1])
    print(top5[2])
    print(top5[3])
    print(top5[4])
