from ce.components.card import Card
from ce.champions.champion import Champion
from ce.components.bonus_card import BonusCard
from ce.components.talent_tray import TalentTray
from ce.components.individual_board import IndividualBoard
from base_player import PlayerBase
from typing import List


class CEPlayer:
    def __init__(self, player, champion):
        self.player: PlayerBase = player
        self.champion: Champion = champion
        self.talents: TalentTray = TalentTray(1, 1, 1, 1, 1)
        self.hand: List[Card] = []
        self.board: IndividualBoard = IndividualBoard()
        self.bonus_cards: List[BonusCard] = []

    def give_cards(self, cards: List[Card]):
        for card in cards:
            self.hand.append(card)

    def give_bonus_card(self, bonus: BonusCard):
        self.bonus_cards.append(bonus)

    def give_bonus_cards(self, bonuses: List[BonusCard]):
        for card in bonuses:
            self.give_bonus_card(card)
