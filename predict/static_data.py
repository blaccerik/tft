import json


class Static:
    champ_labels = {"None": 0,
                    "tft5_aatrox": 1,
                    "tft5_aphelios": 2,
                    "tft5_ashe": 3,
                    "tft5_brand": 4,
                    "tft5_darius": 5,
                    "tft5_diana": 6,
                    "tft5_draven": 7,
                    "tft5_garen": 8,
                    "tft5_gragas": 9,
                    "tft5_hecarim": 10,
                    "tft5_heimerdinger": 11,
                    "tft5_ivern": 12,
                    "tft5_jax": 13,
                    "tft5_kalista": 14,
                    "tft5_karma": 15,
                    "tft5_katarina": 16,
                    "tft5_kayle": 17,
                    "tft5_kennen": 18,
                    "tft5_khazix": 19,
                    "tft5_kindred": 20,
                    "tft5_kled": 21,
                    "tft5_leblanc": 22,
                    "tft5_leesin": 23,
                    "tft5_leona": 24,
                    "tft5_lissandra": 25,
                    "tft5_lulu": 26,
                    "tft5_lux": 27,
                    "tft5_mordekaiser": 28,
                    "tft5_morgana": 29,
                    "tft5_nautilus": 30,
                    "tft5_nidalee": 31,
                    "tft5_nocturne": 32,
                    "tft5_nunu": 33,
                    "tft5_pantheon": 34,
                    "tft5_poppy": 35,
                    "tft5_rell": 36,
                    "tft5_riven": 37,
                    "tft5_ryze": 38,
                    "tft5_sejuani": 39,
                    "tft5_sett": 40,
                    "tft5_soraka": 41,
                    "tft5_syndra": 42,
                    "tft5_taric": 43,
                    "tft5_teemo": 44,
                    "tft5_thresh": 45,
                    "tft5_trundle": 46,
                    "tft5_udyr": 47,
                    "tft5_varus": 48,
                    "tft5_vayne": 49,
                    "tft5_velkoz": 50,
                    "tft5_viego": 51,
                    "tft5_viktor": 52,
                    "tft5_vladimir": 53,
                    "tft5_volibear": 54,
                    "tft5_warwick": 55,
                    "tft5_yasuo": 56,
                    "tft5_ziggs": 57,
                    "tft5_zyra": 58}

    # here are some known comps
    comp0 = ([0], [0])  # null
    comp1 = ([14, 4, 33, 12, 38, 58, 20, 54], [40, 20, 11, 44])  # abo reve
    comp2 = ([9, 41, 31, 37, 12, 15, 8, 54], [1, 24, 42, 45, 37, 44])  # dawn invo
    comp3 = ([10, 30, 45, 16, 7, 36, 38, 51], [49, 48, 29, 6, 28])  # forg iron
    comp4 = ([56, 46, 23, 29, 34, 6, 28, 20], [14, 39, 26, 5, 2])  # night dragon
    comp5 = ([30, 45, 27, 36, 43, 8, 17, 20], [1, 24, 42, 37, 3, 38])  # redee kngiht
    comp6 = {"final": [24, 30, 42, 48, 27, 36, 50, 20],
             "early": [49, 8, 17, 43, 1, 12],
             "mid": []}  # redeem ranger
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

    # comps = {0: comp0,
    #          1: comp1,
    #          2: comp2,
    #          3: comp3,
    #          4: comp4,
    #          5: comp5,
    #          6: comp6,
    #          7: comp7,
    #          8: comp8,
    #          9: comp9,
    #          10: comp10,
    #          11: comp11,
    #          12: comp12,
    #          13: comp13,
    #          14: comp14,
    #          15: comp15,
    #          16: comp16,
    #          17: comp17,
    #          18: comp18,
    #          19: comp19,
    #          20: comp20}

    comps = {0: {"final": tuple(),"early": tuple(),"mid": tuple()},
             1: comp6}  # null
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

    def read_comps(self, link):
        with open(link) as json_file:
            data = json.load(json_file)
            for p in data:
                lista = self.translate_name_to_id(p["final"])
                listb = self.translate_name_to_id(p["early"])
                listc = self.translate_name_to_id(p["mid"])
                for i in lista:
                    if i in listb:
                        listb.remove(i)
                    if i in listc:
                        listc.remove(i)
                for i in listb:
                    if i in listc:
                        listc.remove(i)
                key = max(self.comps)
                self.comps[key + 1] = {"final": tuple(lista),
                                       "early": tuple(listb),
                                       "mid": tuple(listc)}

    def translate_name_to_id(self, input):
        lista = []
        for i in input:
            if "-" in i:
                i = i.replace("-", "")
            name = f"tft5_{i.lower()}"
            id = self.champ_labels[name]
            lista.append(id)
        return lista

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
        with open('C:/Users/theerik/PycharmProjects/tft/data/champions.json') as json_file:
            data = json.load(json_file)
            for p in range(len(data)):
                a = data[p]["championId"].lower()
                print(f'"{a}": {p + 1},')


if __name__ == '__main__':
    s = Static()
    # s.start()
    s.read("C:/Users/theerik/PycharmProjects/tft/data/champions.json")
    s.read_comps("C:/Users/theerik/PycharmProjects/tft/data/comps.json")
    # s.number_to_names((53, 21, 40, 29, 33, 34, 16, 0, 0, 0))
