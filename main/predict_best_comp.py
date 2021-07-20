from static_data import Static, item_to_parts

class Predict:
    def __init__(self, static):
        self.s = static
        # self.s.comps
        # print(self.comps.keys())
        # self.champion_to_traits = self.s.champion_to_traits
        # self.trait_to_champions = self.s.trait_to_champions
        # self.id_to_tier = self.s.id_to_tier
        # self.id_to_champ = self.s.id_to_champ
        # self.id_to_item = self.s.id_to_item
        # self.link_to_csv = link_to_csv

    def get_same_items_and_champs(self, champions: dict, items: list, comp_dict: dict):
        core_champs = comp_dict["needed_champs"].copy()
        start_champs = comp_dict["early_champs"].copy()
        extra_champs = comp_dict["extra_champs"].copy()
        core_champs_size = len(core_champs)
        start_champs_size = len(start_champs)
        extra_champs_size = len(extra_champs)

        core_items = comp_dict["needed_items"].copy()
        core_parts = comp_dict["needed_parts"].copy()
        core_parts_size = len(core_items) * 2

        extra_items = comp_dict["extra_items"].copy()
        extra_parts = comp_dict["extra_parts"].copy()
        extra_parts_size = len(extra_items) * 2

        # if no items are presented
        # 1 comp has that
        if core_parts_size == 0:
            core_parts_size = 1
        if extra_parts_size == 0:
            extra_parts_size = 1


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

        # print("----")
        # print("items", items)
        # print("ci",core_items)
        # print("cp",core_parts)
        # print("ei",extra_items)
        # print("ep",extra_parts)
        # print("-----")
        # if comes error that could not remove then something is wrong with data, look out for shadow/normal items
        # sometimes it says that 2 normal itemas are priority but it shows that champions need to have 1 shadow item for example
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
               core_champs_size, start_champs_size, extra_champs_size, \
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
        tier = self.s.champ_id_to_tier[id]
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

    def predict_main(self, champions: dict,
                     items: list,
                     other_comps=None,
                     many=5):
        """

        :param champions: champion ids
        :param items: item ids
        :param size_of_game_queue:
        :return:
        """
        if other_comps is None:
            other_comps = {}
        top5 = []

        size = len(champions)
        if size == 0:
            size = 1
        size_i = len(items)
        # print(self.s.comps.keys())
        for key in self.s.comps:
            comp_dict = self.s.comps[key]
            name = comp_dict["name"]
            tier = self.get_comp_tier(name)

            # if null comp
            if len(comp_dict) == 1:
                continue

            # print(champions)
            # print(items)
            # print(comp_dict)

            core_count, start_count, extra_count, \
            core_champs_size, start_champs_size, extra_champs_size, \
            core_i, core_p, core_parts_size, \
            extra_i, extra_p, extra_parts_size = self.get_same_items_and_champs(champions, items, comp_dict)

            # print("-----.")
            # print(core_count, start_count, extra_count)
            # print(core_i, core_p, core_parts_size)
            # print(extra_i, extra_p, extra_parts_size)

            # calculate the final score for sort
            # change here
            core_size = self.find_size(core_count, champions)
            start_size = self.find_size(start_count, champions)
            extra_size = self.find_size(extra_count, champions)

            if key in other_comps:
                nerf_level = other_comps[key]
            else:
                nerf_level = 0

            score = self.find_score_for_comp(core_size, start_size, extra_size,
                            core_champs_size, start_champs_size, extra_champs_size, size,
                            core_i, extra_i, core_p, extra_p, core_parts_size, extra_parts_size,
                            tier, nerf_level)

            top5.append((round(score, 3), key, core_size, start_size, extra_size, size,
                         core_i, core_p, extra_i, extra_p, size_i))
            top5.sort(key=lambda x: x[0], reverse=True)
            if len(top5) > many:
                del top5[many]

            # info
            # print(key, name)
        return top5

    def find_score_for_comp(self, core_size, start_size, extra_size,
                            core_champs_size, start_champs_size, extra_champs_size, size,
                            core_i, extra_i, core_p, extra_p, core_parts_size, extra_parts_size,
                            tier, nerf_level):
        """
        Find the %/score for comp on how likely its to be built
        """
        score1 = 1 * core_size / (size) + \
                 0.8 * start_size / (size) + \
                 0.7 * extra_size / (size)

        # item score
        score2 = 1 * core_i / (core_parts_size * 0.5) + \
                 0.9 * extra_i / (extra_parts_size * 0.5) + \
                 0.95 * core_p / (core_parts_size) + \
                 0.8 * extra_p / (extra_parts_size)

        score = tier * (1.0 * score1 + 1.0 * score2 + 0.001)

        if nerf_level == 0:
            final_score = 1 * score
        elif nerf_level == 1:
            final_score = 0.9 * score
        elif nerf_level == 2:
            final_score = 0.8 * score
        else:
            final_score = 0.5 * score
        return final_score

def same_length(top5):
    print("score key cs   ss   es   s ci cp ei ep is")
    for top in top5:
        scr = "{:2.3f}".format(top[0])
        key = "{:2}".format(top[1])
        a = "{:2.2f}".format(top[2])
        b = "{:2.2f}".format(top[3])
        c = "{:2.2f}".format(top[4])
        s = "{:2}".format(top[5])
        sa = "{:2}".format(top[6])
        sb = "{:2}".format(top[7])
        sc = "{:2}".format(top[8])
        sd = "{:2}".format(top[9])
        ss = "{:2}".format(top[10])
        print(scr, key, a,b,c,s,sa,sb,sc,sd,ss)


if __name__ == '__main__':
    s = Static()
    p = Predict(s)
    # p.s.number_to_names(
    #     (1,)
    # )

    top5 = p.predict_main(
        # {26: 2, 44: 1, 24: 1, 48: 1, 1: 1},
        {1: 3},
        [],
        # {2:1}
    )
    print(top5)
    same_length(top5)
