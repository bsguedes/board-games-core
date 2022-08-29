from game import Game
from random import shuffle, sample
from typing import List, Dict, Any
from base_player import PlayerBase
from ce.player import CEPlayer
from ce.states.ce_choose_resources import CEChooseResources
from ce.states.ce_player_turn import CEPlayerTurn
from ce.states.ce_draw_card import CEDrawCard
from ce.states.ce_draw_card_paying_money import CEDrawCardPayingMoney
from ce.states.ce_earn_money import CEEarnMoney
from ce.states.ce_earn_money_paying_talent import CEEarnMoneyPayingTalent
from ce.states.ce_pay_money import CEPayMoney
from ce.states.ce_play_card_upgrade_champion import CEPlayCardUpgradeChampion
from ce.states.ce_take_talent import CETakeTalent
from ce.states.ce_take_talent_paying_card import CETakeTalentPayingCard
from ce.states.ce_choose_row_to_play_card import CEChooseRowToPlayCard
from ce.states.ce_pay_cards import CEPayCards
from ce.states.ce_pay_talents import CEPayTalents
from ce.states.ce_common_state import CECommonState
from ce.champions.champion import Channel
from ce.components.deck import Deck
from ce.components.stage import Stage
from ce.components.objective_board import ObjectiveBoard
from ce.components.bonus_deck import BonusDeck
from ce.db.loader import Loader
from state_machine import GameState

ROUNDS = 4
TURNS = 8


class ClassificacaoEtaria(Game):
    def __init__(self, parameters):
        Game.__init__(self, 'Classificação Etária', parameters)
        loader: Loader = Loader()
        self.deck: Deck = Deck(loader.Cards)
        self.bonus_cards: BonusDeck = BonusDeck(loader.Bonus)
        self.objective_board: ObjectiveBoard = ObjectiveBoard(loader.Objectives)
        self.stage: Stage = Stage()
        self.player_objects: List[CEPlayer] = []
        self.channels: List[Channel] = loader.Channels
        shuffle(self.channels)

    def setup_game(self):
        self.player_objects = [CEPlayer(p, sample(c.Champions, 1)[0]) for p, c in zip(self.players, self.channels)]
        shuffle(self.player_objects)
        for ce_player in self.player_objects:
            ce_player.give_cards(self.deck.draw_cards(5))
            ce_player.give_bonus_cards(self.bonus_cards.draw_cards(2))
        for ce_player in self.player_objects:
            self.state_machine.add_to_end(GameState('ChooseResources', ce_player.player))
        n = len(self.player_objects)

        def turn_cleanup():
            self.deck.replenish_contracts()

        for i in range(ROUNDS):
            for j in range(TURNS - i):
                for k in range(n):
                    turn = self.player_objects[(k + i) % n].player
                    turn_state = GameState('PlayerTurn', turn, {'Round': i, 'Turn': j})
                    turn_state.add_state_cleanup(turn_cleanup)
                    self.state_machine.add_to_end(turn_state)
        self.state_machine.add_to_end(GameState('Over', self.player_objects[0].player))

    def apply_option_on_current_state_game(self, player: PlayerBase, option: Dict[str, Any], state: GameState):
        ce_player = next(p for p in self.player_objects if p.player == player)
        ce_state: CECommonState = self.load_state_for_player(player)
        new_states: List[GameState] = ce_state.ce_apply_option(player, ce_player, option)
        if len(new_states) > 0:
            self.state_machine.add_states_to_next(new_states)

    def next_player_state(self, player, current_player, state):
        return globals()['CE%s' % state.name](player, current_player,
                                              self.deck, self.bonus_cards.number_of_cards(),
                                              self.objective_board, self.stage, self.player_objects, state.args)

    def readable_parameters(self):
        pass
