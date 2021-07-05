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
        self.id_to_tier = {}

    def read(self, link):
        with open(link) as json_file:
            data = json.load(json_file)
            for nr in range(len(data)):
                p = data[nr]
                name = p['championId'].lower()
                tier = p["cost"] - 1
                self.id_to_tier[nr + 1] = tier
                self.champ_to_id[name] = nr + 1
                self.id_to_champ[nr + 1] = name

                traits = list(map(lambda x: x.lower(), p['traits']))
                self.champion_to_traits[name] = traits
                for i in traits:
                    i = i.lower()
                    if i in self.trait_to_champions:
                        self.trait_to_champions[i].append(name)
                    else:
                        self.trait_to_champions[i] = [name]

    def read_items(self, link):
        with open(link) as json_file:
            data = json.load(json_file)
            for p in data:
                name = p["name"].lower()
                id = p["id"]
                self.item_to_id[name] = id
                self.id_to_item[id] = name

    def read_traits(self, link):
        with open(link) as json_file:
            data = json.load(json_file)
            for p in data:
                name = p["key"].lower()
                sets = p["sets"]
                lista = []
                for i in sets:
                    lista.append(i["min"])
                self.trait_to_sets[name] = lista

    def read_comps(self, link):
        with open(link) as json_file:
            data = json.load(json_file)
            for p in data:
                lista = self.translate_name_to_id(p[0])
                listb = self.translate_name_to_id(p[1])
                listc = self.translate_name_to_id(p[2])
                for i in lista:
                    if i in listb:
                        listb.remove(i)
                    if i in listc:
                        listc.remove(i)
                for i in listb:
                    if i in listc:
                        listc.remove(i)
                key = max(self.comps)
                self.comps[key + 1] = (tuple(lista), tuple(listb), tuple(listc))

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
                    champ = ("tft5_" + obj).replace(" ", "")
                    if champ in self.champ_to_id:
                        needed_champs.append(self.champ_to_id[champ])
                    else:
                        # might change if i want items to overlap
                        a = self.item_to_id[obj]
                        # if a not in needed_items:
                        extra_items.append(a)
                        item_to_parts(a, extra_parts)
                # print(max(self.comps) + 1)
                # print(needed_items)
                # print(extra_items)
                for item in needed_items:
                    if item in extra_items:
                        extra_items.remove(item)
                for part in needed_parts:
                    extra_parts.remove(part)

                # figure out rest of the champs
                early_champs = []
                extra_champs = []
                # might need to change if i want champs to overlap
                for champ in early:
                    a = self.champ_to_id[("tft5_" + champ).replace(" ", "")]
                    if a not in needed_champs:
                        early_champs.append(a)
                for champ in options:
                    a = self.champ_to_id[("tft5_" + champ).replace(" ", "")]
                    if a not in needed_champs and a not in early_champs:
                        extra_champs.append(a)

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
        # print(self.comps)

    def translate_name_to_id(self, input):
        lista = []
        for i in input:
            if "-" in i:
                i = i.replace("-", "")
            name = f"tft5_{i.lower()}"
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

def item_to_parts(item, needed_parts):
    # for normal items
    if item < 100:
        for d in str(item):
            needed_parts.append(int(d))
    # for shadow items
    else:
        normal = item % 1000
        parts = [int(d) for d in str(normal)]
        for d in parts:
            needed_parts.append(d)
        for index in range(len(parts)):
            item = parts[index] + 1000
            needed_parts.append(item)


if __name__ == '__main__':
    s = Static()
    # s.start()
    s.read("C:/Users/theerik/PycharmProjects/tft/data/champions.json")
    s.read_items("C:/Users/theerik/PycharmProjects/tft/data/items.json")
    s.read_traits("C:/Users/theerik/PycharmProjects/tft/data/traits.json")
    s.read_comps_tftactics("C:/Users/theerik/PycharmProjects/tft/data/comps_tactics.json")
    # print(s.champ_to_id)
    # print(s.id_to_champ)
    # print(s.champion_to_traits)
    # print(s.trait_to_champions)
    # s.read_comps("C:/Users/theerik/PycharmProjects/tft/data/comps.json")
    # s.number_to_names(
    #     (19, 9, 41, 31, 12, 8, 0, 0, 0, 0)
    # )
    # print(s.translate_name_to_id(["leona", "warwick"]))
