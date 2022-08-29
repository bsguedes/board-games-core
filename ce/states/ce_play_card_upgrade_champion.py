from ce.states.ce_common_state import CECommonState
from base_player import PlayerBase
from ce.components.objective_board import ObjectiveBoard
from ce.components.deck import Deck
from ce.components.stage import Stage
from ce.player import CEPlayer
from typing import List, Dict, Any
from state_machine import GameState


class CEPlayCardUpgradeChampion(CECommonState):
    def __init__(self, player: PlayerBase, current_player: PlayerBase,
                 deck: Deck, bonus_num: int, obj_board: ObjectiveBoard,
                 stage: Stage, player_objects: List[CEPlayer], args: Dict[str, Any]):
        CECommonState.__init__(self, player, current_player, deck, bonus_num, obj_board, stage, player_objects)

    def your_options_game(self):
        options = []
        if self.ce_player.board.ChampionLevel < 4:
            target_level = self.ce_player.champion.Levels[self.ce_player.board.ChampionLevel]
            cash_cost = target_level.CashCost
            talent_cost = target_level.TalentCost
            card_cost = target_level.CardCost
            if (cash_cost == 0 or self.ce_player.board.total_cash() >= cash_cost) and \
               (all(c for t, c in talent_cost.items() if c == 0) or self.ce_player.talents.can_pay(talent_cost)) and \
               (card_cost == 0 or len(self.ce_player.hand) > 0):
                options.append({
                    'Action': 'Upgrade',
                    'CardCost': card_cost,
                    'CashCost': cash_cost,
                    'TalentCost': talent_cost
                })
        if len(options) > 0:
            options.append({'Action': 'Cancel'})
        return options

    def ce_apply_option(self, player: PlayerBase, ce_player: CEPlayer, option: Dict[str, Any]) -> List[GameState]:
        next_states = []
        if option['Action'] == 'Upgrade':
            next_states = option['CashCost'] * [GameState('PayMoney', player)]
            next_states += [GameState('PayCards', player, option['CardCost'])]
            if any(n > 0 for t, n in option['TalentCost']):
                next_states += [GameState('PayTalents', player, option['TalentCost'])]
            ce_player.board.ChampionLevel += 1
        return next_states
