class ChampionList:

    def __init__(self, size):
        self.champions = set()
        self.size = size

    def add(self, champ) -> bool:
        self.champions.add(champ)
        if len(self.champions) == self.size:
            return True
        return False
