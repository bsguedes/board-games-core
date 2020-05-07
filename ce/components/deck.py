from random import shuffle


class Deck:
    def __init__(self):
        self.cards = []
        self.contracts = [None, None, None]

    def shuffle(self):
        shuffle(self.cards)

    def draw_card(self):
        return self.draw_cards(1)[0]

    def draw_cards(self, amount):
        cards = self.cards[len(self.cards)-amount:]
        self.cards = self.cards[:len(self.cards)-amount]
        return cards

    def replenish_contracts(self):
        for i in range(len(self.contracts)):
            if self.contracts[i] is None:
                self.contracts[i] = self.draw_card()
