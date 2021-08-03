import time

class Math:
    def __init__(self, static):
        """
        Wiki:
        tier:  0  1  2  3  4
        size: 29 22 18 12 10

        tier:  0  1  2  3  4
        lv 1 100  0  0  0  0
           2 100  0  0  0  0
           3  75 25  0  0  0
           4  55 30 15  0  0
           5  45 33 20  2  0
           6  25 40 30  5  0
           7  19 30 35 15  1
           8  15 20 35 25  5
           9  12 16 30 30 12 <- differs from ingame
        """
        self.s = static
        # change if needed
        self.tier_list = [29, 22, 18, 12, 10]
        self.level_dict = {
            1: [100, 0, 0, 0, 0],
            2: [100, 0, 0, 0, 0],
            3: [75, 25, 0, 0, 0],
            4: [55, 30, 15, 0, 0],
            5: [45, 33, 20, 2, 0],
            6: [25, 40, 30, 5, 0],
            7: [19, 30, 35, 15, 1],
            8: [15, 20, 35, 25, 5],
            9: [10, 15, 30, 30, 15]
        }

    def calculate(self, level, my_champs, all_champs):
        """
        seen_champs must include my_champs:
        {1: 2} and {1: 3} -> two 1's are mine and one 1 is owned by others

        Find % of each champion in the store
        :return: dict
        key - champ id
        value - list of %'s for each lvl for that champ:
        { 1: [1 ,0.5, 0.01] } -> id 1 (aatrox) lvl 1 is obtained, 0.5% for lvl 2 and 0.01% for lvl 3
        """
        tiers = [1, 3, 9]
        tier_dict = {0: {}, 1: {}, 2: {}, 3: {}, 4: {}}
        for i in self.s.champ_id_to_tier:
            # find aqq tier
            y = 0
            n = 0
            if i in my_champs:
                y = my_champs[i]
            # find miss
            if i in all_champs:
                n = all_champs[i]
            # find how many needed
            t1 = max(tiers[0] - y, 0)
            t2 = max(tiers[1] - y, 0)
            t3 = max(tiers[2] - y, 0)
            # find left
            tier = self.s.champ_id_to_tier[i]
            value = self.tier_list[tier]
            tier_dict[tier][i] = (value - n, t1, t2, t3)
            # print(i, value, n)
        # print(tier_dict)
        final_dict = {}
        for tier in tier_dict:
            sub_dict = tier_dict[tier]
            total = 0
            for i in sub_dict:
                total += sub_dict[i][0]
            for i in sub_dict:
                values = sub_dict[i]
                left = values[0]
                a = values[1]
                b = values[2]
                c = values[3]
                lastup = 1
                lastdown = 1
                a1 = 1
                b1 = 1
                c1 = 1
                for t in range(c):
                    lastup = lastup * (left - t)
                    lastdown = lastdown * (total - t)
                    if t == a - 1:
                        a1 = lastup / lastdown
                    elif t == b - 1:
                        b1 = lastup / lastdown
                    elif t == c - 1:
                        c1 = lastup / lastdown
                    # b = (a - t) / (total) ** (t + 1)
                    # print(".---")
                    # print(lastup, lastdown)
                    # print(lastup / lastdown)
                    # print(b)
                prob = self.level_dict[level][tier] / 100
                # prob = 1
                if a1 != 1:
                    a1 *= prob
                else:
                    a1 *= 0.5

                if b1 != 1:
                    b1 *= prob
                else:
                    b1 *= 1

                if c1 != 1:
                    c1 *= prob
                else:
                    c1 *= 1.5
                final_dict[i] = (a1, b1, c1)
                # break
            # break
        # print(final_dict)

        """
        1: 19 , 2:29
        t = 48
        1 -> 19 / 48
        2 -> 29 / 48
        need 2:
        19 * 18 / 48 * 47
        
        """
        return final_dict
            # print(self.s.id_to_champ[i], i, a)


if __name__ == '__main__':
    m = Math()
    last_time = time.time()
    # 3 ashe
    a = m.calculate(1, {1:1, 4:3}, {1:1, 4:3})
    print("time:", time.time() - last_time)
    time.sleep(0.01)
    print(a)
    # for i in a:
    #     print(i, a[i])
    # m.calculate(3, {7:10, 10:10, 15:10, 34:10, 40:10, 42:10, 46:10})
