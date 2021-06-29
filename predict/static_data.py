import json


class Static:
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

    # here are some known comps
    comp0 = ([0], [0])  # null
    comp1 = ([14, 4, 33, 12, 38, 58, 20, 54], [40, 20, 11, 44])  # abo reve
    comp2 = ([9, 41, 31, 37, 12, 15, 8, 54], [1, 24, 42, 45, 37, 44])  # dawn invo
    comp3 = ([10, 30, 45, 16, 7, 36, 38, 51], [49, 48, 29, 6, 28])  # forg iron
    comp4 = ([56, 46, 23, 29, 34, 6, 28, 20], [14, 39, 26, 5, 2])  # night dragon
    comp5 = ([30, 45, 27, 36, 43, 8, 17, 20], [1, 24, 42, 37, 3, 38])  # redee kngiht
    comp6 = ([24, 30, 42, 48, 27, 36, 50, 20], [49, 8, 17, 43, 1, 12])  # redeem ranger
    comp7 = ([42, 12, 15, 36, 8, 11, 44, 54], [1, 24, 45, 37, 9, 41])  # reve invo

    comp8 = ([55, 4, 40, 33, 12, 38, 11, 54], [14, 58, 20, 3])  # abo brawl
    comp9 = ([52, 4, 27, 33, 58, 36, 38, 50], [14, 40, 30, 26, 20])   # abo spell
    comp10 = ([25, 22, 29, 32, 6, 12, 51, 54], [53, 19, 16])  # coven assa
    comp11 = ([25, 53, 22, 29, 41, 12, 15, 54], [32, 20, 11])  # coven rene
    comp12 = ([18, 46, 23, 34, 13, 6, 28, 51], [9, 47, 55, 31, 36, 5])  # drgn skr
    comp17 = ([4, 10, 30, 39, 45, 53, 36, 21], [0])  # forg caval
    comp15 = ([21, 35, 18, 26, 12, 11, 44, 54], [57, 20])  # hell reve
    comp18 = ([30, 29, 2, 6, 28, 36, 5, 20], [14, 39, 23, 56, 27, 38])  # night ranger
    comp20 = ([30, 58, 12, 15, 36, 43, 50, 17], [1, 24, 42, 45, 37, 54, 27, 38, 8])  # redem spell
    comp19 = ([19, 22, 16, 32, 6, 12, 51, 54], [25, 53, 29])  # reve assa

    comp13 = ([49, 10, 45, 52, 36, 38, 20, 51], [30, 48, 16])  # forg rang
    comp14 = ([1, 37, 56, 6, 7, 28, 43, 17], [14, 39, 23, 29])  # dragon legion
    comp16 = ([47, 40, 3, 58, 12, 11, 20, 54], [55, 57, 43, 36, 50, 44])  # drgonic care

    comps = {0: comp0,
             1: comp1,
             2: comp2,
             3: comp3,
             4: comp4,
             5: comp5,
             6: comp6,
             7: comp7,
             8: comp8,
             9: comp9,
             10: comp10,
             11: comp11,
             12: comp12,
             13: comp13,
             14: comp14,
             15: comp15,
             16: comp16,
             17: comp17,
             18: comp18,
             19: comp19,
             20: comp20}


    champion_to_traits = {}
    trait_to_champions = {}

    def read(self, link):
        with open(link) as json_file:
            data = json.load(json_file)
            for p in data:
                name = p['championId']
                traits = p['traits']
                self.champion_to_traits[name] = traits
                for i in traits:
                    if i in self.trait_to_champions:
                        self.trait_to_champions[i].append(name)
                    else:
                        self.trait_to_champions[i] = [name]

    def number_to_names(self, lista):
        final_list = []
        for i in lista:
            for n in self.champ_labels:
                if self.champ_labels[n] == i:
                    final_list.append(n)
        print(final_list)


    def start(self):
        """
        used to create dict in the console which can be used to create the labels
        :return:
        """
        with open('../pictures/set5/champions.json') as json_file:
            data = json.load(json_file)
            for p in range(len(data)):
                a = data[p]["championId"]
                print(f'"{a}": {p + 1},')


if __name__ == '__main__':
    s = Static()
    s.number_to_names((53, 21, 40, 29, 33, 34, 16, 0, 0, 0))
