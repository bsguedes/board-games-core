from random import shuffle


class BonusDeck:
    def __init__(self):
        self.cards = []

    def shuffle(self):
        shuffle(self.cards)

    def draw_cards(self, amount):
        cards = self.cards[len(self.cards)-amount:]
        self.cards = self.cards[:len(self.cards)-amount]
        return cards
