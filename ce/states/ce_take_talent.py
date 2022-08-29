from ce.states.ce_common_state import CECommonState
from base_player import PlayerBase
from ce.components.objective_board import ObjectiveBoard
from ce.components.deck import Deck
from ce.components.stage import Stage
from ce.player import CEPlayer
from typing import List, Dict, Any
from state_machine import GameState


class CETakeTalent(CECommonState):
    def __init__(self, player: PlayerBase, current_player: PlayerBase,
                 deck: Deck, bonus_num: int, obj_board: ObjectiveBoard,
                 stage: Stage, player_objects: List[CEPlayer], args: Dict[str, Any]):
        CECommonState.__init__(self, player, current_player, deck, bonus_num, obj_board, stage, player_objects)

    def your_options_game(self):
        options = []
        if self.stage.can_reroll():
            options.append({'Action': 'Reroll'})
        for die_face in self.stage.upper_faces_on_stage():
            for face_option in die_face.split('/'):
                options.append({
                    'Action': 'TakeDie',
                    'Die': die_face,
                    'Talent': face_option
                })
        return options

    def ce_apply_option(self, player: PlayerBase, ce_player: CEPlayer, option: Dict[str, Any]) -> List[GameState]:
        new_states = []
        if option['Action'] == 'Reroll':
            self.stage.reroll_all_dice()
            new_states = [GameState('TakeTalent', player)]
        elif option['Action'] == 'TakeDie':
            ce_player.talents.add_talent(option['Talent'], 1)
            self.stage.take_die(option['Die'])
        return new_states
