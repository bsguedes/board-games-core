from ce.states.ce_common_state import CECommonState
from base_player import PlayerBase
from ce.components.objective_board import ObjectiveBoard
from ce.components.deck import Deck
from ce.components.stage import Stage
from ce.player import CEPlayer
from typing import List, Dict, Any
from state_machine import GameState


class CEPlayerTurn(CECommonState):
    def __init__(self, player: PlayerBase, current_player: PlayerBase,
                 deck: Deck, bonus_num: int, obj_board: ObjectiveBoard,
                 stage: Stage, player_objects: List[CEPlayer], args: Dict[str, Any]):
        self.args = args
        CECommonState.__init__(self, player, current_player, deck, bonus_num, obj_board, stage, player_objects)
        self.ce_player.current_turn = self.args['Turn'] + 1
        self.ce_player.current_round = self.args['Round'] + 1

    def as_dict_game(self):
        state_contents = self.args
        state_contents.update(super().as_dict_game())
        return state_contents

    def your_options_game(self):
        options = list()
        talents, optional, position = self.ce_player.board.top_action()
        options.append({'Action': 'TalentHunt', 'TalentCount': talents, 'Optional': optional, 'Position': position})
        cash, optional, position = self.ce_player.board.mid_action()
        if len(self.ce_player.board.cards_in_board()) > 0:
            options.append({'Action': 'ShowAds', 'CashCount': cash, 'Optional': optional, 'Position': position})
        cards, optional, position = self.ce_player.board.bot_action()
        options.append({'Action': 'RecruitAttractions', 'CardCount': cards, 'Optional': optional, 'Position': position})
        for playable_card in self.ce_player.playable_cards():
            options.append({'Action': 'PlayCard', 'PlayableCard': playable_card})
        return options

    def ce_apply_option(self, player: PlayerBase, ce_player: CEPlayer, option: Dict[str, Any]) -> List[GameState]:
        new_states = []
        if option['Action'] == 'TalentHunt':
            talents, optional, index = ce_player.board.top_action()
            new_states = talents * [GameState('TakeTalent', player)]
            if len(ce_player.hand) > 0:
                new_states += optional * [GameState('TakeTalentPayingCard', player)]
            # add states for possible triggers from other players to happen after turn end
        elif option['Action'] == 'ShowAds':
            money, optional, index = ce_player.board.mid_action()
            new_states = min(money, ce_player.board.cash_space()) * [GameState('EarnMoney', player)]
            if len(ce_player.talents.talents_as_array()) > 0 and ce_player.board.cash_space() > money:
                new_states += optional * [GameState('EarnMoneyPayingTalent', player)]
            # add states for possible triggers from other players to happen after turn end
        elif option['Action'] == 'RecruitAttractions':
            cards, optional, index = ce_player.board.bot_action()
            new_states = cards * [GameState('DrawCard', player)]
            if ce_player.board.total_cash() > 0:
                new_states += optional * [GameState('DrawCardPayingMoney', player)]
            # add states for possible triggers from other players to happen after turn end
        elif option['Action'] == 'PlayCard':
            playable_card = option['PlayableCard']
            new_states = [GameState('ChooseRowToPlayCard', player,
                                    {
                                        'Rows': playable_card.ValidRows,
                                        'CashCosts': playable_card.CashCost,
                                        'Card': playable_card.ID
                                    })]
        return new_states
