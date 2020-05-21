from random import shuffle
from typing import List
from ce.components.bonus_card import BonusCard


class BonusDeck:
    def __init__(self, bonus_list):
        self.cards: List[BonusCard] = bonus_list
        self.shuffle_bonus()

    def shuffle_bonus(self) -> None:
        shuffle(self.cards)

    def draw_cards(self, amount) -> List[BonusCard]:
        cards = self.cards[len(self.cards)-amount:]
        self.cards = self.cards[:len(self.cards)-amount]
        return cards
