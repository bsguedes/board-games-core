from ce.states.ce_common_state import CECommonState
from base_player import PlayerBase
from ce.components.objective_board import ObjectiveBoard
from ce.components.deck import Deck
from ce.components.stage import Stage
from ce.player import CEPlayer
from typing import List, Dict, Any
from state_machine import GameState


class CETakeTalentPayingCard(CECommonState):
    def __init__(self, player: PlayerBase, current_player: PlayerBase,
                 deck: Deck, bonus_num: int, obj_board: ObjectiveBoard,
                 stage: Stage, player_objects: List[CEPlayer], args: Dict[str, Any]):
        CECommonState.__init__(self, player, current_player, deck, bonus_num, obj_board, stage, player_objects)

    def your_options_game(self):
        options = [{
            'Action': 'Cancel'
        }]
        for card in self.ce_player.hand:
            options.append({
                'Action': 'DiscardCard',
                'Card': card.ID
            })
        return options

    def ce_apply_option(self, player: PlayerBase, ce_player: CEPlayer, option: Dict[str, Any]) -> List[GameState]:
        new_states = []
        if option['Action'] == 'DiscardCard':
            ce_player.hand = [card for card in ce_player.hand if card.ID != option['Card']]
            new_states = [GameState('TakeTalent', player)]
        return new_states
