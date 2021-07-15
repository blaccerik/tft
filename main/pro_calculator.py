import pickle

from static_data import Static

class Calculator:
    def __init__(self, link_to_json, link_to_csv):
        s = Static()
        s.read_champions(link_to_json)
        self.champion_to_traits = s.champion_to_traits
        self.trait_to_champions = s.trait_to_champions
        self.champ_to_id = s.champ_to_id
        self.id_to_champ = s.id_to_champ
        self.link_to_csv = link_to_csv

    def visualize(self):
        with open('edited_data.pkl', 'rb') as f:
            training_data = pickle.load(f)
        lista = list(self.trait_to_champions.keys())
        dicta = {}
        for i in lista:
            # win, loss
            dicta[i] = (0, 0)
        wl_list = [(4, 0),
                   (3, 0),
                   (2, 0),
                   (1, 0),
                   (0, 1),
                   (0, 2),
                   (0, 3),
                   (0, 4)]
        for row in training_data:
            for comp_nr in range(len(row)):
                comp = row[comp_nr]
                for champ_id in comp:
                    if champ_id != 0:
                        trait_list = self.champion_to_traits[self.id_to_champ[champ_id]]
                        for trait in trait_list:
                            stat = dicta[trait]
                            w = stat[0]
                            l = stat[1]
                            stat2 = wl_list[comp_nr]
                            w2 = stat2[0]
                            l2 = stat2[1]
                            dicta[trait] = (w + w2, l + l2)
        for i in dicta:
            stat = dicta[i]
            w = stat[0]
            l = stat[1]
            score = w / (w + l)
            dicta[i] = score
        items = list(dicta.items())
        items.sort(key=lambda x: x[1], reverse=True)
        print(items)

        for i in lista:
            # win, loss
            dicta[i] = (0, 0)

        for row in training_data:
            for comp_nr in range(len(row)):
                if self.clear(row):
                    comp = row[comp_nr]
                    for champ_id in comp:
                        if champ_id != 0:
                            trait_list = self.champion_to_traits[self.id_to_champ[champ_id]]
                            for trait in trait_list:
                                stat = dicta[trait]
                                w = stat[0]
                                l = stat[1]
                                stat2 = wl_list[comp_nr]
                                w2 = stat2[0]
                                l2 = stat2[1]
                                dicta[trait] = (w + w2, l + l2)
        for i in dicta:
            stat = dicta[i]
            w = stat[0]
            l = stat[1]
            score = w / (w + l)
            dicta[i] = score
        items = list(dicta.items())
        items.sort(key=lambda x: x[1], reverse=True)
        print(items)


    def clear(self, row):
        f1 = 0
        f2 = 0
        for comp in row:
            for id in comp:
                if id != 0:
                    trait_list = self.champion_to_traits[self.id_to_champ[id]]
                    if 'set5_coven' in trait_list:
                        f1 += 1
                    if 'set5_hellion' in trait_list:
                        f2 += 1
        return f1 > 2 and f2 > 2

if __name__ == '__main__':
    c = Calculator("C:/Users/theerik/PycharmProjects/tft/data/champions.json",
                  "C:/Users/theerik/PycharmProjects/tft/data/data.csv")
    c.visualize()

