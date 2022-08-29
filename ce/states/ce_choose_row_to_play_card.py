from ce.states.ce_common_state import CECommonState
from base_player import PlayerBase
from ce.components.objective_board import ObjectiveBoard
from ce.components.deck import Deck
from ce.components.stage import Stage
from ce.player import CEPlayer
from typing import List, Dict, Any
from state_machine import GameState


class CEChooseRowToPlayCard(CECommonState):
    def __init__(self, player: PlayerBase, current_player: PlayerBase,
                 deck: Deck, bonus_num: int, obj_board: ObjectiveBoard,
                 stage: Stage, player_objects: List[CEPlayer], args: Dict[str, Any]):
        self.valid_rows: List[str] = args['Rows']
        self.cash_costs: List[int] = args['CashCosts']
        self.card_id: int = args['Card']
        CECommonState.__init__(self, player, current_player, deck, bonus_num, obj_board, stage, player_objects)

    def as_dict_game(self):
        state_contents = {
            'ValidRows': [
                {
                    'Row': row,
                    'CashCost': cost,
                    'Card': self.card_id
                } for row, cost in zip(self.valid_rows, self.cash_costs)]
        }
        state_contents.update(super().as_dict_game())
        return state_contents

    def your_options_game(self):
        options = [
            {
                'Action': 'ChooseRow',
                'Row': row,
                'CashCost': cost,
                'Card': self.card_id
            } for row, cost in zip(self.valid_rows, self.cash_costs)]
        return options

    def ce_apply_option(self, player: PlayerBase, ce_player: CEPlayer, option: Dict[str, Any]) -> List[GameState]:
        row = option['Row']
        cash_cost = option['CashCost']
        card_id = option['Card']
        card = next(c for c in ce_player.hand if c.ID == card_id)
        new_states = cash_cost * [GameState('PayMoney', player)]
        if card.cost_type() != 'None':
            new_states += [GameState('PayTalents', player, card.Cost)]
        if len(new_states) > 0:
            def play_card_continuation():
                ce_player.board.add_card_to_row(card, row)
                ce_player.hand.remove(card)

            new_states[-1].add_continuation(play_card_continuation)
        else:
            ce_player.board.add_card_to_row(card, row)
            ce_player.hand.remove(card)
        return new_states
