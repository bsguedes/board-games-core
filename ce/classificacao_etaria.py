from game import Game
from random import shuffle, sample
from typing import List, Dict, Any
from base_player import PlayerBase
from ce.player import CEPlayer
from ce.states.ce_choose_resources import CEChooseResources
from ce.states.ce_player_turn import CEPlayerTurn
from ce.champions.champion import Channel
from ce.components.deck import Deck
from ce.components.stage import Stage
from ce.components.objective_board import ObjectiveBoard
from ce.components.bonus_deck import BonusDeck
from ce.db.loader import Loader
from state_machine import GameState
from exceptions import InvalidStateException

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
        self.channels: List[Channel] = loader.Champions

    def setup_game(self):
        self.player_objects = [CEPlayer(player, sample(corp)[0]) for player, corp in zip(self.players, self.channels)]
        shuffle(self.player_objects)
        for ce_player in self.player_objects:
            ce_player.give_cards(self.deck.draw_cards(5))
            ce_player.give_bonus_cards(self.bonus_cards.draw_cards(2))
        for ce_player in self.player_objects:
            self.state_machine.add(GameState('ChooseResources', ce_player.player))
        n = len(self.player_objects)
        for i in range(ROUNDS):
            for j in range(TURNS - i):
                for k in range(n):
                    self.state_machine.add(GameState('PlayerTurn', self.player_objects[(k + i) % n].player))
        self.state_machine.add(GameState('Over', self.player_objects[0].player))

    def apply_option_on_current_state_game(self, player: PlayerBase, option: Dict[str, Any], state: GameState):
        ce_player = next(p for p in self.player_objects if p.player == player)
        if state.name == 'ChooseResources':
            ce_player.bonus_cards = [card for card in ce_player.bonus_cards if card.ID == option['BonusCard']]
            ce_player.hand = [c for c in ce_player.hand if c.ID in option['Cards']]
            for talent in option['Talents']:
                ce_player.talents.add_talent(talent, 1)
        pass

    def next_player_state(self, player, current_player, state):
        if state.name == 'ChooseResources':
            return CEChooseResources(player, current_player,
                                     self.deck, self.bonus_cards.number_of_cards(),
                                     self.objective_board, self.stage, self.player_objects)
        if state.name == 'PlayerTurn':
            return CEPlayerTurn(player, current_player,
                                self.deck, self.bonus_cards.number_of_cards(),
                                self.objective_board, self.stage, self.player_objects)
        else:
            raise InvalidStateException()

    def readable_parameters(self):
        pass
