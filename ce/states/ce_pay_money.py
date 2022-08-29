from ce.states.ce_common_state import CECommonState
from base_player import PlayerBase
from ce.components.objective_board import ObjectiveBoard
from ce.components.deck import Deck
from ce.components.stage import Stage
from ce.player import CEPlayer
from typing import List, Dict, Any
from state_machine import GameState


class CEPayMoney(CECommonState):
    def __init__(self, player: PlayerBase, current_player: PlayerBase,
                 deck: Deck, bonus_num: int, obj_board: ObjectiveBoard,
                 stage: Stage, player_objects: List[CEPlayer], args: Dict[str, Any]):
        CECommonState.__init__(self, player, current_player, deck, bonus_num, obj_board, stage, player_objects)

    def your_options_game(self):
        options = [{
            'Action': 'DiscardCash',
            'CashOrigin': board_card.ID
        } for board_card in self.ce_player.board.cards_with_cash()]
        return options

    def ce_apply_option(self, player: PlayerBase, ce_player: CEPlayer, option: Dict[str, Any]) -> List[GameState]:
        new_states = []
        if option['Action'] == 'DiscardCash':
            slot = next(s for s in ce_player.board.slots_with_cards_in_board() if s.Card.ID == option['CashOrigin'])
            slot.Cash -= 1
            new_states = [GameState('DrawCard', player)]
        return new_states
