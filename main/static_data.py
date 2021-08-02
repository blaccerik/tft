import itertools
import json
from path_manager import Path

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

        p = Path()

        # champ -> id
        # id -> champ
        # id -> tier
        # id -> traits
        # trait -> id
        self.read_champions(p.path_champions_json)

        # item -> id
        # id -> item
        self.read_items(p.path_items_json)

        # trait -> sets : ranger: [2,4] -> ranger needs 2 units for 1st tier and 4 for 2nd
        self.read_traits(p.path_traits_json)
        # print(self.item_to_id)
        # read traits from tftactics json file
        # translate them to proper data like champs, items and parts
        self.read_comps_tftactics(p.path_tactics_json, only_s=False)
        # moba comps
        self.read_comps_moba(p.path_moba_json, only_s=False)

    def read_champions(self, link):
        with open(link) as json_file:
            data = json.load(json_file)
            for nr in range(len(data)):
                p = data[nr]
                name = p['championId'][5:].lower()
                tier = p["cost"] - 1
                # print(name)

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

        self.shadow = {}
        self.short_names = {}

        with open(link) as json_file:
            data = json.load(json_file)
            for p in data:
                name = p["name"].lower().replace(" ", "").replace("'", "").replace(".", "").replace("-", "")
                id = p["id"]
                # change here
                if id < 1000:
                    self.item_to_id[name] = id
                    self.id_to_item[id] = name
                self.shadow[name] = id
        # adding some "custom" names to dict
        self.item_to_id["sword"] = 1
        self.item_to_id["bow"] = 2
        self.item_to_id["rod"] = 3
        self.item_to_id["tear"] = 4
        self.item_to_id["vest"] = 5
        self.item_to_id["cloak"] = 6
        self.item_to_id["belt"] = 7
        self.item_to_id["health"] = 7
        self.item_to_id["gloves"] = 9
        self.short_names[1] = "swor"
        self.short_names[2] = "bow"
        self.short_names[3] = "rod"
        self.short_names[4] = "tear"
        self.short_names[5] = "vest"
        self.short_names[6] = "cloa"
        self.short_names[7] = "belt"
        self.short_names[8] = "spat"
        self.short_names[9] = "glov"

        # :/
        # 'hextechgunblade': 13
        self.item_to_id["hextechlifeblade"] = 13
        self.item_to_id["urfangelsstaff"] = 34
        self.item_to_id["glamorousgauntlet"] = 39
        self.item_to_id["warmogspride"] = 77
        self.item_to_id["runaanstempest"] = 26
        self.item_to_id["dvarapalastoneplate"] = 56
        self.item_to_id["moremoreellonimicon"] = 37
        self.item_to_id["moremoreellonomicon"] = 37
        self.item_to_id["guardianarchangel"] = 15
        self.item_to_id["hellionemblem"] = 28
        self.item_to_id["locketoftargonprime"] = 35
        self.item_to_id["statikkfavor"] = 24
        self.item_to_id["fistoffairness"] = 49
        self.item_to_id["luminousdeathblade"] = 11
        self.item_to_id["sunlightcape"] = 57
        # self.item_to_id[""] = 35
        # self.item_to_id[""] = 35




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

    def read_comps_tftactics(self, link, only_s=True):
        with open(link) as json_file:
            data = json.load(json_file)
            for row in data:
                name = row["name"]

                # if name != 'SAbomination RevenantsSlow Roll':
                #     continue

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
                    item = item.replace(" ", "").replace("'", "").replace(".", "")
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
                item_to_champ = []
                last_champ = None
                for obj in lista:
                    # print(self.champ_to_id)
                    champ = obj.replace(" ", "").replace("'", "")
                    if champ in self.champ_to_id:
                        champ_id = self.champ_to_id[champ]
                        last_champ = champ_id
                        needed_champs.append(champ_id)
                    elif champ in self.item_to_id:
                        # might change if i want items to overlap
                        a = self.item_to_id[champ]
                        extra_items.append(a)
                        item_to_champ.append((a, last_champ))
                    else:
                        print("error", champ)

                # remove copies
                for i in needed_items:
                    if i in extra_items:
                        extra_items.remove(i)
                # find parts
                for i in extra_items:
                    item_to_parts(i, extra_parts)

                # figure out rest of the champs
                early_champs = set()
                extra_champs = set()
                # might need to change if i want champs to overlap
                for champ in early:
                    champ = champ.replace(" ", "")
                    if champ in self.champ_to_id:
                        a = self.champ_to_id[champ]
                        if a not in needed_champs:
                            early_champs.add(a)
                    else:
                        print("error", champ)
                # print(options)
                for champ in options:
                    champ = champ.replace(" ", "")
                    if champ in self.champ_to_id:
                        a = self.champ_to_id[champ]
                        if a not in needed_champs and a not in early_champs:
                            extra_champs.add(a)
                    else:
                        print("error", champ)
                early_champs = list(early_champs)
                extra_champs = list(extra_champs)

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
                    "item_to_champ": item_to_champ
                }
                # break

    def read_comps_moba(self, link, only_s=True):
        with open(link) as json_file:
            data = json.load(json_file)
            for row in data:
                # print(row)
                name = row["name"].lower()
                tier = row["letter"]
                if only_s:
                    if tier != "s":
                        continue
                name = tier + name

                final = row["final"]
                parts_order = row["item order"]
                all_items = row["all items"]
                options = row["options"]
                mid = row["mid"]
                early = row["early"]

                # figure out champs
                needed_champs = []
                early_champs = []
                extra_champs = []
                for i in final:
                    ii = i.replace("-", "").lower()
                    if ii in self.champ_to_id:
                        needed_champs.append(self.champ_to_id[ii])
                for i in early:
                    ii = i.replace("-", "").lower()
                    if ii in self.champ_to_id:
                        a = self.champ_to_id[ii]
                        if a not in needed_champs:
                            early_champs.append(a)
                for i in mid:
                    ii = i.replace("-", "").lower()
                    if ii in self.champ_to_id:
                        a = self.champ_to_id[ii]
                        if a not in needed_champs and a not in early_champs:
                            extra_champs.append(a)
                for i in options:
                    ii = i.replace("-", "").lower()
                    if ii in self.champ_to_id:
                        a = self.champ_to_id[ii]
                        if a not in needed_champs and a not in early_champs and a not in extra_champs:
                            extra_champs.append(a)
                # figure out core items
                needed_items = []
                needed_parts = []
                extra_items = []
                extra_parts = []
                lista = []
                for part in parts_order:
                    part = part.replace("-", "").lower()
                    id = self.item_to_id[part]
                    lista.append(id)
                listb = []
                for item_list in all_items:
                    # if error change text in json
                    champ = item_list[1].replace(" ", "").replace("'", "").lower()
                    item = item_list[0].replace("-", "").replace(" ", "").replace("'", "").lower()
                    if item == "handofvengence":
                        item = "handofvengeance"
                    elif item == "archdemonsstaff":
                        item = "archdemonsstaffofimmortality"

                    # change
                    id = self.item_to_id[item]
                    champ_id = self.champ_to_id[champ]
                    # id = self.shadow[item]

                    # remove shadow trait
                    id = id % 100
                    listb.append((id, champ_id))
                # core
                item_to_champ = []
                self.find_core_items(lista, listb, item_to_champ)
                # needed_items.append(k[0])
                for i in item_to_champ:
                    listb.remove(i)
                    a = i[0] % 10
                    b = i[0] // 10
                    needed_items.append(i[0])
                    needed_parts.append(a)
                    needed_parts.append(b)
                # extra
                for i in listb:
                    a = i[0] % 10
                    b = i[0] // 10
                    extra_items.append(i[0])
                    extra_parts.append(a)
                    extra_parts.append(b)
                    item_to_champ.append(i)
                # print(needed_items)
                # print(needed_parts)
                # print(extra_items)
                # print(extra_parts)
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
                    "item_to_champ": item_to_champ
                }
                # break

    def find_core_items(self, lista, listb, item_to_champ):
        item_count = max(len(listb) // 3, 2)
        n = 0
        for i in range(len(lista)):
            for j in range(i + 1):
                id1 = lista[j]
                id2 = lista[i]
                id = min(id1 * 10 + id2, id2 * 10 + id1)
                for k in listb:
                    if id == k[0]:
                        n += 1
                        # needed_items.append(k)
                        item_to_champ.append(k)
                        if n == item_count:
                            return
                        break

    def adjust_start_extra(self, start_champs, extra_champs):
        lista = []
        for i in start_champs:
            if self.champ_id_to_tier[i] > 1:
                lista.append(i)
        for i in lista:
            start_champs.remove(i)
            extra_champs.append(i)
        lista = []
        for i in extra_champs:
            if self.champ_id_to_tier[i] < 2:
                lista.append(i)
        for i in lista:
            extra_champs.remove(i)
            start_champs.append(i)

    def find_best_champs(self, my_tier_0_1, all_tier_0_1, current_traits_0_1, need_start, start_champs):
        # remove overlap
        for i in my_tier_0_1:
            if i in all_tier_0_1:
                all_tier_0_1.remove(i)
        indexes = list(range(0, len(all_tier_0_1)))
        # find the index combination
        best_score = 0
        best_champs = []
        for combination in itertools.combinations(indexes, need_start):
            current_traits_copy = current_traits_0_1.copy()
            # find modified traits
            champs = []
            for i in combination:
                champ = all_tier_0_1[i]
                traits = self.champion_to_traits[champ]
                champs.append(champ)
                for trait in traits:
                    if trait in current_traits_copy:
                        current_traits_copy[trait] += 1
                    else:
                        current_traits_copy[trait] = 1
            # score
            points = 0
            for i in current_traits_copy:
                value = current_traits_copy[i]
                sets = self.trait_to_sets[i]
                for j in sets:
                    if value >= j:
                        points += 1
                    else:
                        if value > 2 and value not in sets:
                            points += 0.5
                        break
            # find best score
            if points > best_score:
                best_score = points
                best_champs = [combination]
            elif points == best_score:
                best_champs.append(combination)
        # add champs to list
        for i in best_champs:
            for j in i:
                champ = all_tier_0_1[j]
                if champ not in start_champs:
                    start_champs.append(champ)

    def find_traits(self, core_champs, start_champs, extra_champs):

        """
        0,1 <= core + start
        0,1 => start + x, x: len(start) == 3

        5 + 1
        5 + 1 + x(2) => max traits

        list (possible)
        find all comibinations => list = [0,1,2]
        => 01 02 12
        find traits with them
        find "score"
        sort
        find best
        """

        min_number_of_champions = 2

        need_start = max(min_number_of_champions - len(start_champs), 0)
        need_extra = max(min_number_of_champions - len(extra_champs) - 1, 0)

        # find lists with specific tiers
        all_tier_0_1 = []
        all_tier_2_3_4 = []
        for i in self.champ_id_to_tier:
            tier = self.champ_id_to_tier[i]
            if tier < 2:
                all_tier_0_1.append(i)
            else:
                all_tier_2_3_4.append(i)

        all_champs = core_champs + start_champs + extra_champs
        current_traits_0_1 = {}
        current_traits_2_3_4 = {}
        my_tier_0_1 = []
        my_tier_2_3_4 = []
        # sort champs to tiers and find their traits
        for i in all_champs:
            a = self.champion_to_traits[i]
            tier = self.champ_id_to_tier[i]
            if tier < 2:
                my_tier_0_1.append(i)
                for j in a:
                    if j in current_traits_0_1:
                        current_traits_0_1[j] += 1
                    else:
                        current_traits_0_1[j] = 1
            elif tier == 2:
                my_tier_2_3_4.append(i)
                for j in a:
                    if j in current_traits_0_1:
                        current_traits_0_1[j] += 1
                    else:
                        current_traits_0_1[j] = 1
            else:
                my_tier_2_3_4.append(i)
            for j in a:
                if j in current_traits_2_3_4:
                    current_traits_2_3_4[j] += 1
                else:
                    current_traits_2_3_4[j] = 1
        # print(current_traits_0_1)
        self.find_best_champs(my_tier_0_1, all_tier_0_1, current_traits_0_1, need_start, start_champs)
        self.find_best_champs(my_tier_2_3_4, all_tier_2_3_4, current_traits_2_3_4, need_extra, extra_champs)


    def adjust_comps(self):
        for comp_key in self.comps:
            comp = self.comps[comp_key]
            if len(comp) == 1:
                continue
            # print(comp["name"])
            core_champs = comp["needed_champs"]
            start_champs = comp["early_champs"]
            extra_champs = comp["extra_champs"]
            # print("----")
            # print(core_champs)
            # print(start_champs)
            # print(extra_champs)
            self.adjust_start_extra(start_champs, extra_champs)
            # print("----")
            # core_champs = comp["needed_champs"]
            # start_champs = comp["early_champs"]
            # extra_champs = comp["extra_champs"]
            # print(core_champs)
            # print(start_champs)
            # print(extra_champs)
            self.find_traits(core_champs, start_champs, extra_champs)
            # print("----")
            # core_champs = comp["needed_champs"]
            # start_champs = comp["early_champs"]
            # extra_champs = comp["extra_champs"]
            # print(core_champs)
            # print(start_champs)
            # print(extra_champs)
            # self.number_to_names(core_champs)
            # self.number_to_names(start_champs)
            # self.number_to_names(extra_champs)
            # break

def item_to_parts(item, needed_parts):
    # for normal items
    a = item % 10
    b = item // 10
    needed_parts.append(a)
    needed_parts.append(b)


if __name__ == '__main__':
    s = Static()
    # s.start()
    # s.only_letters()


    # # print()
    # print(s.champ_to_id)
    # print(s.id_to_champ)
    # print(s.champion_to_traits)
    # print(s.trait_to_champions)
    # print(s.item_to_id)
    # print(s.id_to_item)
    # print(s.champ_id_to_tier)
    # print(s.id_to_item)
    # print(s.trait_to_sets)
    #
    # for i in s.comps:
    #     a = s.comps[i]
    #     print(i, a)

    s.adjust_comps()

    print("comps:")
    for i in s.comps:
        a = s.comps[i]
        if len(a) == 1:
            continue
        # print(a)
        print(i, a["needed_champs"], a['early_champs'], a['extra_champs'])
        break

    # s.read_comps("C:/Users/theerik/PycharmProjects/tft/data/comps.json")
    # s.number_to_names(
    #     (19, 9, 41, 31, 12, 8, 0, 0, 0, 0)
    # )
    # print(s.translate_name_to_id(["leona", "warwick"]))
