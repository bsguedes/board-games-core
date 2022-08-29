from ce.states.ce_common_state import CECommonState
from base_player import PlayerBase
from ce.components.objective_board import ObjectiveBoard
from ce.components.deck import Deck
from ce.components.stage import Stage
from ce.player import CEPlayer
from typing import List, Dict, Any
from itertools import combinations, product
from state_machine import GameState


class CEChooseResources(CECommonState):
    def __init__(self, player: PlayerBase, current_player: PlayerBase,
                 deck: Deck, bonus_num: int, obj_board: ObjectiveBoard,
                 stage: Stage, player_objects: List[CEPlayer], args: Dict[str, Any]):
        CECommonState.__init__(self, player, current_player, deck, bonus_num, obj_board, stage, player_objects)

    def your_options_game(self):
        bonus_cards = self.ce_player.bonus_cards
        cards = self.ce_player.hand
        talents = ['X1', 'X2', 'X3', 'X4', 'X5']
        options = []
        for i in range(6):
            p_c = list(combinations(cards, i))
            t_c = list(combinations(talents, 5 - i))
            for opt in list(product(p_c, t_c)):
                for j in range(2):
                    options.append({
                        'BonusCard': bonus_cards[j].ID,
                        'Cards': [c.ID for c in opt[0]],
                        'Talents': list(opt[1])
                    })
        return options

    def ce_apply_option(self, player: PlayerBase, ce_player: CEPlayer, option: Dict[str, Any]) -> List[GameState]:
        ce_player.bonus_cards = [card for card in ce_player.bonus_cards if card.ID == option['BonusCard']]
        ce_player.hand = [c for c in ce_player.hand if c.ID in option['Cards']]
        for talent in option['Talents']:
            ce_player.talents.add_talent(talent, 1)
        return []
