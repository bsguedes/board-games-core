from random import shuffle
from typing import List
from ce.components.card import Card


class Deck:
    def __init__(self, card_list):
        self.cards: List[Card] = card_list
        self.shuffle_deck()
        self.contracts: List[Card] = self.draw_cards(3)

    def shuffle_deck(self) -> None:
        shuffle(self.cards)

    def draw_card(self) -> Card:
        return self.draw_cards(1)[0]

    def draw_cards(self, amount: int) -> List[Card]:
        cards = self.cards[len(self.cards)-amount:]
        self.cards = self.cards[:len(self.cards)-amount]
        return cards

    def replenish_contracts(self) -> None:
        for i in range(len(self.contracts)):
            if self.contracts[i] is None:
                self.contracts[i] = self.draw_card()

    def number_of_cards(self) -> int:
        return len(self.cards)
