from random import shuffle
from typing import List, Optional
from ce.components.card import Card

NUMBER_OF_CONTRACTS = 4


class Deck:
    def __init__(self, card_list):
        self.cards: List[Card] = card_list
        self.shuffle_deck()
        self.contracts: List[Optional[Card]] = self.draw_cards(NUMBER_OF_CONTRACTS)
        self.discard_pile: List[Card] = []

    def shuffle_deck(self) -> None:
        shuffle(self.cards)

    def draw_card(self) -> Card:
        return self.draw_cards(1)[0]

    def discard(self, card: Card):
        self.discard_pile.append(card)

    def take_from_contracts(self, card_id: int) -> Card:
        for i in range(NUMBER_OF_CONTRACTS):
            if self.contracts[i].ID == card_id:
                card = self.contracts[i]
                self.contracts[i] = None
                return card

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
