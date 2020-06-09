from ce.states.ce_common_state import CECommonState
from base_player import PlayerBase
from ce.components.objective_board import ObjectiveBoard
from ce.components.deck import Deck
from ce.components.stage import Stage
from ce.player import CEPlayer
from typing import List


class CEDrawCardPayingMoney(CECommonState):
    def __init__(self, player: PlayerBase, current_player: PlayerBase,
                 deck: Deck, bonus_num: int, obj_board: ObjectiveBoard,
                 stage: Stage, player_objects: List[CEPlayer]):
        CECommonState.__init__(self, player, current_player, deck, bonus_num, obj_board, stage, player_objects)

    def your_options_game(self):
        options = [{
            'Action': 'BlindDraw',
            'CashOrigin': board_card.ID
        } for board_card in self.ce_player.board.cards_with_cash()]
        options.append({
            'Action': 'Cancel'
        })
        for card in self.deck.contracts:
            if card is not None:
                for board_card in self.ce_player.board.cards_with_cash():
                    options.append({
                        'Action': 'DrawFromContracts',
                        'Card': card.ID,
                        'CashOrigin': board_card.ID
                    })
        return options
