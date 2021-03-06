from ce.states.ce_common_state import CECommonState
from base_player import PlayerBase
from ce.components.objective_board import ObjectiveBoard
from ce.components.deck import Deck
from ce.components.stage import Stage
from ce.player import CEPlayer
from typing import List


class CEEarnMoney(CECommonState):
    def __init__(self, player: PlayerBase, current_player: PlayerBase,
                 deck: Deck, bonus_num: int, obj_board: ObjectiveBoard,
                 stage: Stage, player_objects: List[CEPlayer]):
        CECommonState.__init__(self, player, current_player, deck, bonus_num, obj_board, stage, player_objects)

    def your_options_game(self):
        options = []
        for card in self.ce_player.hand:
            if card.CurrentCash < card.MaxCash:
                options.append({
                    'Action': 'PlaceMoney',
                    'Card': card.ID
                })
        if len(options) > 0:
            options.append({'Action': 'Cancel'})
        return options
