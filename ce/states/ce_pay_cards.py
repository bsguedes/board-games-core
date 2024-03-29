from ce.states.ce_common_state import CECommonState
from base_player import PlayerBase
from ce.components.objective_board import ObjectiveBoard
from ce.components.deck import Deck
from ce.components.stage import Stage
from ce.player import CEPlayer
from typing import List, Dict, Any
from itertools import combinations


class CEPayCards(CECommonState):
    def __init__(self, player: PlayerBase, current_player: PlayerBase,
                 deck: Deck, bonus_num: int, obj_board: ObjectiveBoard,
                 stage: Stage, player_objects: List[CEPlayer], args: Dict[str, Any]):
        self.card_count = args['Count']
        CECommonState.__init__(self, player, current_player, deck, bonus_num, obj_board, stage, player_objects)

    def as_dict_game(self):
        state_contents = {
            'Count': self.card_count
        }
        state_contents.update(super().as_dict_game())
        return state_contents

    def your_options_game(self):
        options = [
            {
                'Action': 'PayCards',
                'Cards': [card.ID for card in cards]
            }
            for cards in combinations(self.ce_player.hand, self.card_count)]
        return options
