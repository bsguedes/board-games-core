from ce.states.ce_common_state import CECommonState
from base_player import PlayerBase
from ce.components.objective_board import ObjectiveBoard
from ce.components.deck import Deck
from ce.components.stage import Stage
from ce.player import CEPlayer
from typing import List


class CETakeTalentPayingCard(CECommonState):
    def __init__(self, player: PlayerBase, current_player: PlayerBase,
                 deck: Deck, bonus_num: int, obj_board: ObjectiveBoard,
                 stage: Stage, player_objects: List[CEPlayer]):
        CECommonState.__init__(self, player, current_player, deck, bonus_num, obj_board, stage, player_objects)

    def your_options_game(self):
        options = [{
            'Action': 'Cancel'
        }]
        if self.stage.can_reroll():
            options.append({'Action': 'Reroll'})
        for die_face in self.stage.upper_faces_on_stage():
            for face_option in die_face.split('-'):
                for card in self.ce_player.hand:
                    options.append({
                        'Action': 'TakeDiePayingCard',
                        'Die': die_face,
                        'Talent': face_option,
                        'Card': card.ID
                    })
        return options
