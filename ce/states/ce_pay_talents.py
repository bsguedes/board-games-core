from ce.states.ce_common_state import CECommonState
from base_player import PlayerBase
from ce.components.objective_board import ObjectiveBoard
from ce.components.deck import Deck
from ce.components.stage import Stage
from ce.player import CEPlayer
from typing import List, Dict, Any
from state_machine import GameState


class CEPayTalents(CECommonState):
    def __init__(self, player: PlayerBase, current_player: PlayerBase,
                 deck: Deck, bonus_num: int, obj_board: ObjectiveBoard,
                 stage: Stage, player_objects: List[CEPlayer], args: Dict[str, Any]):
        self.talent_cost = args
        CECommonState.__init__(self, player, current_player, deck, bonus_num, obj_board, stage, player_objects)

    def as_dict_game(self):
        state_contents = {
            'Talents': [{'Talent': t, 'Cost': f} for t, f in self.talent_cost.items()]
        }
        state_contents.update(super().as_dict_game())
        return state_contents

    def your_options_game(self):
        options = [
            {
                'Action': 'PayTalents',
                'Talents': method
            }
            for method in self.ce_player.talents.payable_methods(self.talent_cost)]
        return options

    def ce_apply_option(self, player: PlayerBase, ce_player: CEPlayer, option: Dict[str, Any]) -> List[GameState]:
        if option['Action'] == 'PayTalents':
            for talent in option['Talents']:
                ce_player.talents.add_talent(talent, -1)
        return []
