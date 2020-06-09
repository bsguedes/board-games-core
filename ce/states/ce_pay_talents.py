from ce.states.ce_common_state import CECommonState
from base_player import PlayerBase
from ce.components.objective_board import ObjectiveBoard
from ce.components.deck import Deck
from ce.components.stage import Stage
from ce.player import CEPlayer
from typing import List, Dict, Any


class CEPayTalents(CECommonState):
    def __init__(self, player: PlayerBase, current_player: PlayerBase,
                 deck: Deck, bonus_num: int, obj_board: ObjectiveBoard,
                 stage: Stage, player_objects: List[CEPlayer], args: Dict[str, Any]):
        CECommonState.__init__(self, player, current_player, deck, bonus_num, obj_board, stage, player_objects)
        self.talent_cost = args['Talents']

    def as_dict_game(self):
        return {
            'Talents': self.talent_cost,
        }.update(super().as_dict_game())

    def your_options_game(self):
        options = [
            {
                'Action': 'PayTalents',
                'Talents': method
            }
            for method in self.ce_player.talents.payable_methods(self.talent_cost)]
        return options
