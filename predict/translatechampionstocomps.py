import operator
import pickle
import random

import numpy as np
from static_data import Static
from predict_best_comp import Predict, same_length

class Translate:
    def __init__(self, link_to_json, link_to_csv, link_to_comps):

        self.p = Predict()

        # s = Static()
        # s.read(link_to_json)
        # s.read_comps(link_to_comps)
        # self.s = s
        # self.comps = s.comps
        # self.champion_to_traits = s.champion_to_traits
        # self.trait_to_champions = s.trait_to_champions
        # self.link_to_csv = link_to_csv

    def make_match(self, one_player_set):
        champions = one_player_set[0]
        items = one_player_set[1]
        # print(champions)
        # print(items)
        top5 = self.p.predict_main(champions,
                                   items,
                                   len(champions),
                                   {},
                                   [],
                                   many=1)
        # same_length(top5)
        if top5[0][1] < 0.6:
            return None
        return top5[0]


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
                top = self.make_match(one_player_set)
                if top is None:
                    if winner is None:
                        break
                    else:
                        continue

                comp = top[1]
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
                array = np.eye(len(self.p.s.comps))[winner]
                final_list.append((np.array(some_list), array))
                for times in range(shuffle):
                    new_data = random.sample(some_list, len(some_list))
                    final_list.append((np.array(new_data), array))
            # break
        np.random.shuffle(final_list)
        np.save("training_comp.npy", final_list)
        print(len(final_list))



if __name__ == '__main__':
    t = Translate("C:/Users/theerik/PycharmProjects/tft/data/champions.json",
                  "C:/Users/theerik/PycharmProjects/tft/data/data.csv",
                  "C:/Users/theerik/PycharmProjects/tft/data/comps.json")
    t.analyze_main(shuffle=5, equal=False)
    # a = t.make_match(
    #     (19, 9, 55)
    # )
    # print(a[0])
    # print(a[1])
    # print(a[2])
    # print(a[3])
    # print(a[4])
