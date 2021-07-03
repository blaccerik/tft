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
        Does not actually find the level but the "score" of the levels
        lvl 1 = 0.5
        lvl 2 = 1
        lvl 3 = 2
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

    def get_comp_tier(self, name):
        letter = name[0].lower
        if letter == "s":
            return 1.3
        elif letter == "a":
            return 1
        else:
            return 0.7

    def find_size(self, count, champions):
        size = 0
        for champ in count:
            nr = champions[champ]
            size += self.find_level(nr, champ)
        return size

    def predict_main(self, champions_in_game: dict,
                     items: list,
                     size_of_game_queue: int,
                     champions_on_bench: dict,
                     champs_in_store: list):
        """

        :param champions_in_game: champion ids [1,5,1,1,4,0]
        :param items: item ids
        :param size_of_game_queue:
        :param champions_on_bench:
        :param champs_in_store:
        :return:
        """
        top5 = []
        if 0 in champions_in_game:
            del champions_in_game[0]
        if 0 in champions_on_bench:
            del champions_on_bench[0]

        # join total champions owned into 1 dict
        champions = dict(champions_in_game)
        for i in champions_on_bench:
            if i in champions:
                champions[i] += champions_on_bench[i]
            else:
                champions[i] = champions_on_bench[i]
        for i in champs_in_store:
            if i in champions:
                champions[i] += 1
            else:
                champions[i] = 1

        size = len(champions)
        size_i = len(items)
        for key in self.comps:
            comp_dict = self.comps[key]
            name = comp_dict["name"]
            tier = self.get_comp_tier(name)

            # if null comp
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

            core_size = self.find_size(core_count, champions)
            start_size = self.find_size(start_count, champions)
            extra_size = self.find_size(extra_count, champions)

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
            print(key, name)
        return top5


if __name__ == '__main__':
    p = Predict()
    p.s.number_to_names(
        (26, 8, 44, 24, 48, 1)
    )
    p.s.number_to_items(
        (1009, 9, 3, 5)
    )
    # print(p.s.champ_to_id["tft5_teemo"])
    # print(p.s.champ_to_id["tft5_warwick"])
    # print(p.s.champ_to_id["tft5_thresh"])
    # print(p.s.id_to_item[99])
    # print(p.s.id_to_item[9])
    # print(p.s.id_to_item[1])
    top5 = p.predict_main(
        {26: 2, 44: 1, 24: 1, 48: 1, 1: 1},
        [],
        # (1009, 9, 3, 5, 2, 5, 1005, 1034),
        5,
        {44: 1},
        [44, 24, 1, 26, 27]
    )
    print("   scr key cs ss es  s ci cp ei ep si")
    print(top5[0])
    print(top5[1])
    print(top5[2])
    print(top5[3])
    print(top5[4])
