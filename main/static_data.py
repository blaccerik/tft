import json

class Static:

    def __init__(self):
        comp0 = {"name": "null"}  # null
        self.comps = {0: comp0}
        self.champion_to_traits = {}
        self.trait_to_champions = {}
        self.trait_to_sets = {}
        self.champ_to_id = {"none": 0}
        self.id_to_champ = {0: "none"}
        self.id_to_item = {}
        self.item_to_id = {}
        self.champ_id_to_tier = {}
        # champ -> id
        # id -> champ
        # id -> tier
        # id -> traits
        # trait -> id
        self.read_champions("C:/Users/theerik/PycharmProjects/tft/data/champions.json")

        # item -> id
        # id -> item
        self.read_items("C:/Users/theerik/PycharmProjects/tft/data/items.json")

        # trait -> sets : ranger: [2,4] -> ranger needs 2 units for 1st tier and 4 for 2nd
        self.read_traits("C:/Users/theerik/PycharmProjects/tft/data/traits.json")

        # read traits from tftactics json file
        # translate them to proper data like champs, items and parts
        self.read_comps_tftactics("C:/Users/theerik/PycharmProjects/tft/data/comps_tactics.json", only_s=False)

    def read_champions(self, link):
        with open(link) as json_file:
            data = json.load(json_file)
            for nr in range(len(data)):
                p = data[nr]
                name = p['championId'][5:].lower()
                tier = p["cost"] - 1

                champ_id = nr + 1

                self.champ_id_to_tier[champ_id] = tier
                self.champ_to_id[name] = champ_id
                self.id_to_champ[champ_id] = name

                traits = list(map(lambda x: x[5:].lower(), p['traits']))
                self.champion_to_traits[champ_id] = traits
                for i in traits:
                    if i in self.trait_to_champions:
                        self.trait_to_champions[i].append(champ_id)
                    else:
                        self.trait_to_champions[i] = [champ_id]

    def read_items(self, link):
        with open(link) as json_file:
            data = json.load(json_file)
            for p in data:
                name = p["name"].lower().replace(" ", "").replace("'", "")
                id = p["id"]
                self.item_to_id[name] = id
                self.id_to_item[id] = name

    def read_traits(self, link):
        with open(link) as json_file:
            data = json.load(json_file)
            for p in data:
                name = p["key"][5:].lower()
                sets = p["sets"]
                lista = []

                for i in sets:
                    lista.append(i["min"])
                self.trait_to_sets[name] = lista

    # def read_comps(self, link):
    #     with open(link) as json_file:
    #         data = json.load(json_file)
    #         for p in data:
    #             lista = self.translate_name_to_id(p[0])
    #             listb = self.translate_name_to_id(p[1])
    #             listc = self.translate_name_to_id(p[2])
    #             for i in lista:
    #                 if i in listb:
    #                     listb.remove(i)
    #                 if i in listc:
    #                     listc.remove(i)
    #             for i in listb:
    #                 if i in listc:
    #                     listc.remove(i)
    #             key = max(self.comps)
    #             self.comps[key + 1] = (tuple(lista), tuple(listb), tuple(listc))

    def read_comps_tftactics(self, link, only_s=True):
        with open(link) as json_file:
            data = json.load(json_file)
            for row in data:
                name = row["name"]
                if only_s:
                    tier = name[0].lower()
                    if tier != "s":
                        continue

                lista = row["final"]
                items = row["item order"]
                options = row["options"]
                early = row["early"]

                # figure out the items
                needed_items = set()
                for item in items:
                    item = item.replace(" ", "").replace("'", "")
                    a = self.item_to_id[item]
                    # check if a is item or part
                    # if in the future they add more parts then
                    # change number here
                    if a % 1000 > 10:
                        needed_items.add(a)
                needed_items = list(needed_items)
                needed_parts = []
                for item in needed_items:
                    item_to_parts(item, needed_parts)

                # figure out extra items and needed champs
                extra_items = []
                extra_parts = []
                needed_champs = []
                for obj in lista:
                    # print(self.champ_to_id)
                    champ = obj.replace(" ", "").replace("'", "")
                    if champ in self.champ_to_id:
                        needed_champs.append(self.champ_to_id[champ])
                    elif champ in self.item_to_id:
                        # might change if i want items to overlap
                        a = self.item_to_id[champ]
                        # if a not in needed_items:
                        extra_items.append(a)
                        item_to_parts(a, extra_parts)
                    else:
                        print("error", champ)
                for item in needed_items:
                    if item in extra_items:
                        extra_items.remove(item)
                for part in needed_parts:
                    if part in extra_parts:
                        extra_parts.remove(part)

                # figure out rest of the champs
                early_champs = []
                extra_champs = []
                # might need to change if i want champs to overlap
                for champ in early:
                    champ = champ.replace(" ", "")
                    if champ in self.champ_to_id:
                        a = self.champ_to_id[champ]
                        if a not in needed_champs:
                            early_champs.append(a)
                    else:
                        print("error", champ)
                for champ in options:
                    champ = champ.replace(" ", "")
                    if champ in self.champ_to_id:
                        a = self.champ_to_id[champ]
                        if a not in needed_champs and a not in early_champs:
                            extra_champs.append(a)
                    else:
                        print("error", champ)

                key = max(self.comps) + 1
                self.comps[key] = {
                    "name": name,
                    "needed_champs": needed_champs,
                    "early_champs": early_champs,
                    "extra_champs": extra_champs,
                    "needed_items": needed_items,
                    "needed_parts": needed_parts,
                    "extra_items": extra_items,
                    "extra_parts": extra_parts,
                }

    def translate_name_to_id(self, input):
        lista = []
        for i in input:
            if "-" in i:
                # lee-sin :(
                i = i.replace("-", "")
            name = i.lower()
            id = self.champ_to_id[name]
            lista.append(id)
        return lista

    def number_to_names(self, lista):
        final_list = []
        for i in lista:
            for n in self.champ_to_id:
                if self.champ_to_id[n] == i:
                    final_list.append(n)
        print(final_list)

    def number_to_items(self, lista):
        final_list = []
        for i in lista:
            final_list.append(self.id_to_item[i])
        print(final_list)

    def only_letters(self):
        """
        used in screen.py
        to only use letters that are in trait names
        :return:
        """
        seta = set()
        for i in self.champion_to_traits:
            seta.update(list(i))
            seta.update(i[0].capitalize())
        # for i in self.trait_to_champions:
        #     seta.update(list(i))
        seta = list(seta)
        seta.sort()
        text = ""
        for i in seta:
            text += i
        print(text)

def item_to_parts(item, needed_parts):
    # for normal items

    if item < 100:
        for d in str(item):
            needed_parts.append(int(d))
    # for shadow items
    else:
        normal = item % 1000
        # parts = [int(d) for d in str(normal)]
        for d in str(normal):
            nr = int(d)
            needed_parts.append(nr)
            needed_parts.append(nr + 1000)


if __name__ == '__main__':
    s = Static()
    # s.start()
    # s.only_letters()


    # print()
    # print(s.champ_to_id)
    # print(s.id_to_champ)
    # print(s.champion_to_traits)
    # print(s.trait_to_champions)
    # print(s.item_to_id)
    # print(s.id_to_item)
    # print(s.champ_id_to_tier)
    # print(s.id_to_item)
    # print(s.trait_to_sets)
    for i in s.comps:
        a = s.comps[i]
        print(a)

    # s.read_comps("C:/Users/theerik/PycharmProjects/tft/data/comps.json")
    # s.number_to_names(
    #     (19, 9, 41, 31, 12, 8, 0, 0, 0, 0)
    # )
    # print(s.translate_name_to_id(["leona", "warwick"]))
