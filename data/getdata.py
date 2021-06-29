import datetime
import time
import requests
from csv import DictWriter
import csv

class GetData:
    def __init__(self, key, link_to_puuids, link_to_matchids, link_to_data):
        self.key = self.read(key, single=True)

        self.link_to_matchids = link_to_matchids
        self.link_to_puuids = link_to_puuids
        self.link_to_data = link_to_data

        self.puuids = self.read(link_to_puuids)
        self.matches = self.read(link_to_matchids)
        self.read_matches = self.read(link_to_data, csv_type=True)

        self.region = "https://europe.api.riotgames.com"
        self.tft_version = 5

    def read(self, link, single=False, csv_type=False):
        if csv_type:
            with open(link, encoding="utf8") as file:
                content = csv.reader(file, delimiter=',')
                next(content)
                seta = set()
                # print(content)
                for row in content:
                    # print(row)
                    # for i in row:
                    #     print(i)
                    # print(row)
                    game_id = row[0]
                    # print(game_id)
                    seta.add(game_id)
                return seta
        else:
            with open(link, encoding="utf8") as file:
                content = file.readlines()
            if single:
                key = content[0]
                return f"?api_key={key}"
            else:
                seta = set()
                for i in content:
                    row = i.strip()
                    seta.add(row)
                return seta

    def read_puuid(self, puuid):
        lista = []
        data = f"/tft/match/v1/matches/by-puuid/{puuid}/ids"
        link = self.region + data + self.key
        response_API = requests.get(link)
        a = response_API.json()
        if type(a) == dict:
            return False
        for i in a:
            code = i
            lista.append(code)
        return lista

    def check_match(self, match):
        if match in self.matches:
            return False
        else:
            return True

    def add_match(self, match):
        if self.check_match(match):
            self.matches.add(match)
            with open(self.link_to_matchids, "a") as file:
                file.write(match)
                file.write("\n")
            return True
        return False

    def check_puuid(self, puuid):
        if puuid in self.puuids:
            return False
        else:
            return True

    def add_puuid(self, puuid):
        if self.check_puuid(puuid):
            self.puuids.add(puuid)
            with open(self.link_to_puuids, "a") as file:
                file.write(puuid)
                file.write("\n")

    def read_match(self, match):
        if match not in self.read_matches:
            data = f"/tft/match/v1/matches/{match}"
            link = self.region + data + self.key
            response_API = requests.get(link)
            a = response_API.json()
            if "status" in a:
                print("failed")
                return False
            else:
                version = a["info"]['tft_set_number']
                if version != self.tft_version:
                    print(match)
                    return None
                game_time = a["info"]["game_datetime"]
                # aa = datetime.datetime.fromtimestamp(game_time / 1000)
                # print(match, aa)
                lista = a["info"]['participants']
                dicta = {'game': match, "time": game_time}
                field_names = ['game', "time", 1, 2, 3, 4, 5, 6, 7, 8]
                with open(self.link_to_data, 'a', newline='') as fd:
                    for i in lista:
                        # print(i)
                        placement = i["placement"]
                        puuid = i["puuid"]
                        last_round = i['last_round']
                        damage_done = i['total_damage_to_players']
                        time_ingame = i['time_eliminated']

                        summoner_dict = {"round": last_round,
                                         "damage": damage_done,
                                         "time": time_ingame}

                        self.add_puuid(puuid)
                        units = i["units"]
                        champions = []
                        for j in units:
                            champ = j['character_id']
                            item_list = j["items"]
                            rarity = j["rarity"]
                            level = j["tier"]
                            some_dict = {"id": champ, "items": item_list, "rarity": rarity, "level": level}
                            champions.append(some_dict)
                        summoner_dict["units"] = champions
                        dicta[placement] = summoner_dict
                    dictwriter_object = DictWriter(fd, fieldnames=field_names)
                    dictwriter_object.writerow(dicta)
                self.read_matches.add(match)
                return True
        else:
            print("read")
            return None

    def get_matches_from_puuids(self):
        lista = list(self.puuids)
        current = 0
        total = 0
        print("total:", len(lista))
        for puuid in lista:
            matches = self.read_puuid(puuid)
            if matches is False:
                print("added:", current, "analysed:", total)
                current = 0
                total = 0
                print("sleeping")
                time.sleep(60)
                print("finished sleeping")
            else:
                for match in matches:
                    value = self.add_match(match)
                    if value:
                        current += 1
                    total += 1

    def get_data_and_puuids_from_match(self):
        matches = list(self.matches - self.read_matches)
        print("total:", len(self.matches))
        print("read:", len(self.read_matches))
        print("left:", len(matches))

        # time
        rate = 120 / 100  # 100 requests every 2 minutes(s)
        total_time = len(matches) * rate  # s
        print("time (s):", total_time)

        current = 0
        total = 0
        for match in matches:

            # read matches only from certain date
            # so it doesnt waste time on read old matches
            nr = int(match[5:])
            # 21
            if nr < 5332230239:  # 06-22
                continue

            a = self.read_match(match)
            if a is False:
                print("added:", current, "analysed:", total)
                current = 0
                total = 0
                print("sleeping")
                time.sleep(60)
                print("finished sleeping")
            elif a is True:
                current += 1
            total += 1


if __name__ == '__main__':
    d = GetData("C:/Users/theerik/PycharmProjects/tft/data/key.txt",
             "C:/Users/theerik/PycharmProjects/tft/data/puuids.txt",
             "C:/Users/theerik/PycharmProjects/tft/data/matches.txt",
             "C:/Users/theerik/PycharmProjects/tft/data/data.csv")
    # get match ids from puuids
    # d.get_matches_from_puuids()

    # get data from match ids
    d.get_data_and_puuids_from_match()

    # these 2 functions are used to get data from riot's database
    # just choose one and let it run as it takes a while for data to be read

    # d.read_match("EUW1_5321353332")
    #
