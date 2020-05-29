from ce.components.card import Card
from ce.champions.champion import Champion
from ce.components.bonus_card import BonusCard
from ce.components.talent_tray import TalentTray
from ce.components.individual_board import IndividualBoard
from ce.common import ROWS
from base_player import PlayerBase
from typing import List
from ce.states.action_playable_card import PlayableCard


class CEPlayer:
    def __init__(self, player, champion):
        self.player: PlayerBase = player
        self.champion: Champion = champion
        self.talents: TalentTray = TalentTray(0, 0, 0, 0, 0)
        self.hand: List[Card] = []
        self.board: IndividualBoard = IndividualBoard()
        self.bonus_cards: List[BonusCard] = []

    def give_cards(self, cards: List[Card]) -> None:
        for card in cards:
            self.hand.append(card)

    def give_bonus_card(self, bonus: BonusCard) -> None:
        self.bonus_cards.append(bonus)

    def give_bonus_cards(self, bonuses: List[BonusCard]) -> None:
        for card in bonuses:
            self.give_bonus_card(card)

    def playable_cards(self) -> List[PlayableCard]:
        cards = []
        for row in ROWS:
            for card in self.hand:
                if self.board.playable(row) and self.talents.playable(card):
                    for method in self.talents.payment_methods(card):
                        cards.append(PlayableCard(card.ID, row, self.board.row_cost(row), method))
        return cards
