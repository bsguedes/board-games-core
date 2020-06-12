from ce.states.ce_common_state import CECommonState
from base_player import PlayerBase
from ce.components.objective_board import ObjectiveBoard
from ce.components.deck import Deck
from ce.components.stage import Stage
from ce.player import CEPlayer
from typing import List


class CEPlayerTurn(CECommonState):
    def __init__(self, player: PlayerBase, current_player: PlayerBase,
                 deck: Deck, bonus_num: int, obj_board: ObjectiveBoard,
                 stage: Stage, player_objects: List[CEPlayer]):
        CECommonState.__init__(self, player, current_player, deck, bonus_num, obj_board, stage, player_objects)

    def your_options_game(self):
        options = list()
        talents, optional = self.ce_player.board.top_action()
        options.append({'Action': 'TalentHunt', 'TalentCount': talents, 'Optional': optional})
        cash, optional = self.ce_player.board.mid_action()
        options.append({'Action': 'ShowAds', 'CashCount': cash, 'Optional': optional})
        cards, optional = self.ce_player.board.bot_action()
        options.append({'Action': 'RecruitAttractions', 'CardCount': cards, 'Optional': optional})
        for playable_card in self.ce_player.playable_cards():
            options.append({'Action': 'PlayCard', 'PlayableCard': playable_card})
        return options
