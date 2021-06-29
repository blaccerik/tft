import csv
import json
import numpy as np
import random

class EditData():
    champ_labels = {"None": 0,
                    "TFT5_Aatrox": 1,
                    "TFT5_Aphelios": 2,
                    "TFT5_Ashe": 3,
                    "TFT5_Brand": 4,
                    "TFT5_Darius": 5,
                    "TFT5_Diana": 6,
                    "TFT5_Draven": 7,
                    "TFT5_Garen": 8,
                    "TFT5_Gragas": 9,
                    "TFT5_Hecarim": 10,
                    "TFT5_Heimerdinger": 11,
                    "TFT5_Ivern": 12,
                    "TFT5_Jax": 13,
                    "TFT5_Kalista": 14,
                    "TFT5_Karma": 15,
                    "TFT5_Katarina": 16,
                    "TFT5_Kayle": 17,
                    "TFT5_Kennen": 18,
                    "TFT5_Khazix": 19,
                    "TFT5_Kindred": 20,
                    "TFT5_Kled": 21,
                    "TFT5_LeBlanc": 22,
                    "TFT5_LeeSin": 23,
                    "TFT5_Leona": 24,
                    "TFT5_Lissandra": 25,
                    "TFT5_Lulu": 26,
                    "TFT5_Lux": 27,
                    "TFT5_Mordekaiser": 28,
                    "TFT5_Morgana": 29,
                    "TFT5_Nautilus": 30,
                    "TFT5_Nidalee": 31,
                    "TFT5_Nocturne": 32,
                    "TFT5_Nunu": 33,
                    "TFT5_Pantheon": 34,
                    "TFT5_Poppy": 35,
                    "TFT5_Rell": 36,
                    "TFT5_Riven": 37,
                    "TFT5_Ryze": 38,
                    "TFT5_Sejuani": 39,
                    "TFT5_Sett": 40,
                    "TFT5_Soraka": 41,
                    "TFT5_Syndra": 42,
                    "TFT5_Taric": 43,
                    "TFT5_Teemo": 44,
                    "TFT5_Thresh": 45,
                    "TFT5_Trundle": 46,
                    "TFT5_Udyr": 47,
                    "TFT5_Varus": 48,
                    "TFT5_Vayne": 49,
                    "TFT5_Velkoz": 50,
                    "TFT5_Viego": 51,
                    "TFT5_Viktor": 52,
                    "TFT5_Vladimir": 53,
                    "TFT5_Volibear": 54,
                    "TFT5_Warwick": 55,
                    "TFT5_Yasuo": 56,
                    "TFT5_Ziggs": 57,
                    "TFT5_Zyra": 58}

    path = "training_data"

    link = "data/data.csv"

    training_data = []

    size_of_champion_queue = 9

    # key is champ/trait get traits/champs
    champions = {}
    traits = {}
    # key is tier, value is list of champs in that rarity group
    rarity = {}

    def start(self):
        """
        used to create dict in the console which can be used to create the labels
        :return:
        """
        with open('pictures/set5/champions.json') as json_file:
            data = json.load(json_file)
            for p in range(len(data)):
                a = data[p]["championId"]
                print(f'"{a}": {p + 1},')
        pass

    def read(self, link):
        with open(link) as json_file:
            data = json.load(json_file)
            for p in data:
                name = p['championId']
                traits = p['traits']
                rare = p["cost"] - 1
                if rare in self.rarity:
                    self.rarity[rare].append(name)
                else:
                    self.rarity[rare] = [name]
                self.champions[name] = traits
                for i in traits:
                    if i in self.traits:
                        self.traits[i].append(name)
                    else:
                        self.traits[i] = [name]

    def decision(self, probability):
        return random.random() < probability

    def should_keep(self, some_list, id, rarity):
        keep_tier_2 = 0.5
        keep_tier_1 = 0.9
        if rarity == 2 and self.decision(keep_tier_2):
            some_list.append(id)
        if rarity == 1 and self.decision(keep_tier_1):
            some_list.append(id)
        if rarity == 0:
            some_list.append(id)
        pass

    def add_more(self, some_list):
        add_tier_0 = 0.6
        add_tier_1 = 0.3
        add_tier_2 = 0.1
        # # remove
        # if self.decision(0.5):
        #     other_size = 5
        # else:
        #     other_size = 4
        #
        # while len(some_list) > other_size:
        #     some_list.remove(random.choice(some_list))

        # add
        if self.decision(0.5):
            this_size = 4
        else:
            this_size = 5
        while len(some_list) < this_size:
            if self.decision(add_tier_0):
                champ = random.choice(self.rarity[0])
                id = self.champ_labels[champ]
                some_list.append(id)
                continue
            if self.decision(add_tier_1):
                champ = random.choice(self.rarity[1])
                id = self.champ_labels[champ]
                some_list.append(id)
                continue
            if self.decision(add_tier_2):
                champ = random.choice(self.rarity[2])
                id = self.champ_labels[champ]
                some_list.append(id)
                continue


    def add_champs(self, row, earl_game, add_remove, shuffle):
        winner_data = None
        other_data = []
        earl_game_range = range(0, 3)  # 0, 1, 2
        earl_game_size = range(5, 7)  # 5, 6

        for summoner_data in row:
            summoner_data = summoner_data.replace("'", '"')
            json_data = json.loads(summoner_data)
            size = len(json_data["units"])
            if winner_data is None:
                winner_data = np.zeros(59, dtype=int)
                for champ_data in json_data["units"]:
                    champ = champ_data["id"]
                    id = self.champ_labels[champ]
                    winner_data[id] = 1
                winner_data[0] = 0
            elif size > self.size_of_champion_queue:
                return None
            else:
                some_list = []
                for champ_data in json_data["units"]:
                    champ = champ_data["id"]
                    id = self.champ_labels[champ]
                    if earl_game:
                        rarity = champ_data["rarity"]
                        if rarity in earl_game_range:
                            if add_remove:
                                self.should_keep(some_list, id, rarity)
                            else:
                                some_list.append(id)
                    else:
                        some_list.append(id)
                if earl_game:
                    list_size = random.choice(earl_game_size)
                    while len(some_list) > list_size:
                        some_list.remove(random.choice(some_list))
                    if add_remove:
                        self.add_more(some_list)
                while len(some_list) < self.size_of_champion_queue:
                    some_list.append(0)
                other_data.append(some_list)
            last_round = json_data["round"]
            damage = json_data["damage"]
            time_ingame = json_data["time"]
        some_list = [other_data]
        for times in range(shuffle):
            new_data = random.sample(other_data, len(other_data))
            some_list.append(new_data)
        final_data = []
        for lista in some_list:
            listc = []
            for listb in lista:
                for id in listb:
                    listc.append(id)
            final_data.append((np.array(listc), winner_data))
        return final_data

    def make_training_data(self,
                           game_time=0,
                           earl_game=False,
                           add_remove=False,
                           shuffle_placements=0,
                           health_left=0,
                           damage=0,
                           round=0):
        """
        :param game_time: which games to keep and which not
        :param earl_game: rarity 0-2
        :param add_remove: if early game comp then remove most tier 3 (blue) champs, some tier 2 (green)
        and add random tier 1 champs
        :param shuffle_placements: shuffle 2-8 place and generate more data
        :param health_left: how much health should the winner have
        :param damage: how much damage did winner do
        :param round: keep only comps did made it to certain round
        :return: list of tuples of training data and targets as numpy arrays
        => [ ( np.array(train_data), np.array(targets) ) ]
        """
        # todo make early game comps where only 2-3 champs are present
        #  use only tier 1-2 maybe 3 champs
        # todo shuffle data per channel section:
        #  [11,12,13, 21,22,23] => [12,11,13, 23,21,22], [11,13,12, 21,23,22] etc
        #  and keep winner data
        # todo keep only where winner liver are big
        with open(self.link, encoding="utf8") as file:
            content = csv.reader(file, delimiter=',')
            # skip title
            next(content)
            for row in content:
                del row[0]
                this_game_time = int(row[0])
                del row[0]
                if this_game_time > game_time:
                    value = self.add_champs(row, earl_game, add_remove, shuffle_placements)
                    if type(value) == list:
                        for tuplea in value:
                            self.training_data.append(tuplea)
            np.random.shuffle(self.training_data)
            np.save("training_data.npy", self.training_data)
            print(len(self.training_data))


if __name__ == '__main__':
    e = EditData()
    e.read("C:/Users/theerik/PycharmProjects/tft/data/champions.json")
    e.make_training_data(earl_game=True, add_remove=True, shuffle_placements=0)