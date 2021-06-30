import csv
import json
import time
from datetime import datetime
import pickle
from static_data import Static

class EditData():
    def __init__(self, link_to_json, link_to_csv):
        s = Static()
        s.read(link_to_json)
        self.champion_to_traits = s.champion_to_traits
        self.trait_to_champions = s.trait_to_champions
        self.champ_labels = s.champ_labels
        self.link_to_csv = link_to_csv
        self.size_of_champion_queue = 10
        # path to csv which has all the data about the matches

    def add_champs(self, row):
        # winner_data = None
        final_data = []

        for summoner_data in row:
            temp_list = []
            summoner_data = summoner_data.replace("'", '"')
            json_data = json.loads(summoner_data)
            size = len(json_data["units"])

            # for future
            last_round = json_data["round"]
            damage = json_data["damage"]
            time_ingame = json_data["time"]

            if size > self.size_of_champion_queue:
                return None
            for champ_data in json_data["units"]:
                champ = champ_data["id"].lower()
                id = self.champ_labels[champ]
                if id in temp_list:
                    return None
                temp_list.append(id)
            while len(temp_list) < self.size_of_champion_queue:
                temp_list.append(0)
            final_data.append(tuple(temp_list))
        return tuple(final_data)

    def make_data(self, game_time=0):
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

        training_data = []

        with open(self.link_to_csv, encoding="utf8") as file:
            content = csv.reader(file, delimiter=',')
            # skip title
            next(content)
            for row in content:
                del row[0]
                this_game_time = int(row[0])
                del row[0]
                if this_game_time > game_time:
                    value = self.add_champs(row)
                    if type(value) == tuple:
                        training_data.append(value)
            # np.random.shuffle(self.training_data)
            # np.save("training_data.npy", self.training_data)
            print(len(training_data))
        with open('edited_data.pkl', 'wb') as f:
            pickle.dump(training_data, f)


if __name__ == '__main__':
    e = EditData("C:/Users/theerik/PycharmProjects/tft/data/champions.json",
                  "C:/Users/theerik/PycharmProjects/tft/data/data.csv")

    date = "23/06/2021"
    date_number = int(time.mktime(datetime.strptime(date, "%d/%m/%Y").timetuple())) * 1000
    e.make_data(game_time=date_number)