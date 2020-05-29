from ce.components.card import Card
from typing import List
from itertools import combinations
from ce.common import sort_and_deduplicate


class TalentTray:
    def __init__(self, x1=0, x2=0, x3=0, x4=0, x5=0):
        self.X1: int = x1
        self.X2: int = x2
        self.X3: int = x3
        self.X4: int = x4
        self.X5: int = x5

    def playable(self, card: Card) -> bool:
        return card.cost_type() == 'None' or len(self.payment_methods(card)) > 0

    def add_talent(self, talent: str, count: int):
        if talent == 'X1':
            self.X1 += count
        elif talent == 'X2':
            self.X2 += count
        elif talent == 'X3':
            self.X3 += count
        elif talent == 'X4':
            self.X4 += count
        elif talent == 'X5':
            self.X5 += count

    def get_talent(self, talent: str) -> int:
        if talent == 'X1':
            return self.X1
        elif talent == 'X2':
            return self.X2
        elif talent == 'X3':
            return self.X3
        elif talent == 'X4':
            return self.X4
        elif talent == 'X5':
            return self.X5

    def talents_as_array(self) -> List[str]:
        return [i for s in [[t] * self.get_talent(t) for t in ['X1', 'X2', 'X3', 'X4', 'X5']] for i in s]

    def payment_methods(self, card: Card) -> List[List[str]]:
        methods = []
        talents = self.talents_as_array()
        if card.cost_type() == 'OR':
            for i in range(1, 3):
                for comb in combinations(talents, i):
                    methods.append(list(comb))
        elif card.cost_type() == 'AND':
            talent_count = sum([int(c) for t, c in card.Cost.items()])
            joker_count = sum([int(c) for t, c in card.Cost.items() if t == 'X'])
            for i in range(talent_count, talent_count * 2 + 1 - joker_count):
                for comb in combinations(talents, i):
                    methods.append(list(sorted(comb)))
        methods = sort_and_deduplicate(methods)
        return [m for m in methods if card.can_be_paid_with(m)]
