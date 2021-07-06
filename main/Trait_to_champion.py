import itertools
import time
from static_data import Static

class Calculator:

    def __init__(self, static):
        self.s = static

    def main(self, traits: dict, count):
        possible_champs = set()
        for key in traits:
            # if key in self.s.trait_to_champions:
            possible_champs.update(self.s.trait_to_champions[key])
        possible_champs = list(possible_champs)
        indexes = list(range(0, len(possible_champs)))
        best_value = 100
        best_way = []
        size_of_traits = len(traits)
        for real_count in range(count, count - 2, -1):
            for combination in itertools.combinations(indexes, real_count):
                copy = traits.copy()
                value = self.check(combination, copy, possible_champs, size_of_traits < 10)
                if value is False:
                    continue
                else:
                    if value < best_value:
                        best_way = [combination]
                        best_value = value
                    elif value == best_value:
                        best_way.append(combination)
            if len(best_way) > 0:
                break
        final = []
        for i in best_way:
            some_list = []
            for j in i:
                some_list.append(possible_champs[j])
            final.append(some_list)
        return final

    def check(self, combination, copy, possible_champs, excact):
        added = 0
        for i in combination:
            champ = possible_champs[i]
            traits = self.s.champion_to_traits[champ]
            for trait in traits:
                if trait in copy:
                    value = copy[trait]
                    if value == 0:
                        return False
                    else:
                        copy[trait] = value - 1
                else:
                    if excact:
                        return False
                    added += 1
        for i in copy.values():
            if i > 0:
                return False
        return added

if __name__ == '__main__':
    s = Static()
    c = Calculator(s)

    # dicta = {"brawler": 2, "forgotten": 2, "knight": 1, "legionnaire": 1, "redeemed": 1, "dawnbringer": 1}
    # dicta = {"dawnbringer": 2, "assassin": 2, "brawler": 1, "ironclad": 1, "knight": 1, "forgotten": 1}
    # dicta = {"coven": 1, "forgotten": 1, "renewer":1,  "legionnaire": 1, "dragonslayer": 1, "spellweaver": 1, "skirmisher": 1,
    #          "abomination": 1}
    # dicta = {"brawler": 2, "knight": 2, "dawnbringer": 2, "redeemed": 2,"invoker": 1, "ironclad": 1, "assassin": 1,  "abomination": 1}

    dicta = {'abomination': 4, 'draconic': 3, 'brawler': 2, 'spellweaver': 2, 'skirmisher': 1, 'mystic': 1, 'forgotten': 1, 'legionnaire': 1}
    a = c.main(dicta, 7)
    for i in a:
        print(i)
