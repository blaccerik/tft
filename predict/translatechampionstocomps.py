import operator
import pickle
import random

import numpy as np
from static_data import Static

class Translate:
    def __init__(self, link_to_json, link_to_csv, link_to_comps):
        s = Static()
        s.read(link_to_json)
        s.read_comps(link_to_comps)
        self.s = s
        self.comps = s.comps
        self.champion_to_traits = s.champion_to_traits
        self.trait_to_champions = s.trait_to_champions
        self.link_to_csv = link_to_csv

    def make_match(self, tuplea):
        top3 = []
        seta = set(tuplea)
        if 0 in seta:
            seta.remove(0)
        size = len(seta)
        if size > 8:
            size = 8
        elif size == 0:
            size = 200

        for key in self.comps:
            # print(key)
            comp_dict = self.comps[key]
            final = comp_dict["final"]
            mid = comp_dict["mid"]
            early = comp_dict["early"]
            # comp_primary = comp_tuple[0]
            # comp_sec = comp_tuple[1]
            high = len(seta.intersection(final))
            med = len(seta.intersection(mid))
            low = len(seta.intersection(early))
            # score = (high + low) / size
            # score = (0.7 * high + 0.2 * med + 0.1 * low)

            score = (high / size) + (med / (2 * size)) + (low / (2 * size))

            top3.append((score, key, high, med, low, size))
            top3.sort(key=lambda x: x[0], reverse=True)
            if len(top3) > 3:
                del top3[3]
        # # print(top3)
        # self.s.number_to_names(seta)
        # print("---")
        # self.s.number_to_names(self.comps[top3[0][1]]["final"])
        # self.s.number_to_names(self.comps[top3[1][1]]["final"])
        return top3


    def analyze_main(self, shuffle=0, equal=False):
        with open('edited_data.pkl', 'rb') as f:
            training_data = pickle.load(f)
        final_list = []

        count = {}
        n = 0
        for one_sett in training_data:
            # n += 1
            # if n == 100:
            #     break
            winner = None
            some_list = []
            for i in range(len(one_sett)):
                one_player_set = one_sett[i]
                # print(one_player_set)
                top3 = self.make_match(one_player_set)
                # print(top3[0])
                # print(top3[1])
                # print(top3[2])
                if top3[0][0] < 0.5:
                    # return
                    if i != 0:
                        some_list.append(0)
                        continue
                    else:
                        break
                comp = top3[0][1]

                if winner is None:
                    winner = comp
                else:
                    some_list.append(comp)
            if winner is not None:
                if winner in count:
                    if equal:
                        value = max(count.items(), key=operator.itemgetter(1))
                        if value[0] == winner:
                            continue
                    count[winner] += 1
                else:
                    count[winner] = 1
                array = np.eye(len(self.comps))[winner]
                final_list.append((np.array(some_list), array))
                for times in range(shuffle):
                    new_data = random.sample(some_list, len(some_list))
                    final_list.append((np.array(new_data), array))
        # print(count)
        np.random.shuffle(final_list)
        np.save("training_comp.npy", final_list)
        print(len(final_list))



if __name__ == '__main__':
    t = Translate("C:/Users/theerik/PycharmProjects/tft/data/champions.json",
                  "C:/Users/theerik/PycharmProjects/tft/data/data.csv",
                  "C:/Users/theerik/PycharmProjects/tft/data/comps.json")
    t.analyze_main(shuffle=0, equal=False)
