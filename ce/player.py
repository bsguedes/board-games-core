from ce.components.token_tray import TokenTray
from ce.components.individual_board import Board


class CEPlayer:
    def __init__(self, player, corporation):
        self.player = player
        self.corporation = corporation
        self.talents = TokenTray(1, 1, 1, 1, 1)
        self.hand = []
        self.board = Board()
        self.bonus_cards = []

    def give_cards(self, cards):
        for card in cards:
            self.hand.append(card)

    def give_bonus_card(self, bonus):
        self.bonus_cards.append(bonus)
