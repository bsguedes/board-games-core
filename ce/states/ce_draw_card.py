from ce.states.ce_common_state import CECommonState
from base_player import PlayerBase
from ce.components.objective_board import ObjectiveBoard
from ce.components.deck import Deck
from ce.components.stage import Stage
from ce.player import CEPlayer
from typing import List, Dict, Any
from state_machine import GameState


class CEDrawCard(CECommonState):
    def __init__(self, player: PlayerBase, current_player: PlayerBase,
                 deck: Deck, bonus_num: int, obj_board: ObjectiveBoard,
                 stage: Stage, player_objects: List[CEPlayer], args: Dict[str, Any]):
        CECommonState.__init__(self, player, current_player, deck, bonus_num, obj_board, stage, player_objects)

    def your_options_game(self):
        options = [{
            'Action': 'BlindDraw'
        }]
        for card in self.deck.contracts:
            if card is not None:
                options.append({
                    'Action': 'DrawFromContracts',
                    'Card': card.ID
                })
        return options

    def ce_apply_option(self, player: PlayerBase, ce_player: CEPlayer, option: Dict[str, Any]) -> List[GameState]:
        if option['Action'] == 'BlindDraw':
            ce_player.hand.append(self.deck.draw_card())
        elif option['Action'] == 'DrawFromContracts':
            ce_player.hand.append(self.deck.take_from_contracts(option['Card']))
        return []
