from game import Game
from random import shuffle, sample
from typing import List
from ce.player import CEPlayer
from ce.champions.champion import Channel
from ce.components.deck import Deck
from ce.components.stage import Stage
from ce.components.objective_board import ObjectiveBoard
from ce.components.bonus import BonusDeck
from ce.db.loader import Loader


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
        for player in self.player_objects:
            player.give_cards(self.deck.draw_cards(5))
            player.give_bonus_card(self.bonus_cards.draw_cards(2))
        return self.player_objects[0].player

    def apply_option_on_current_state_game(self, player, option):
        pass

    def next_player_state(self, player, current_player):
        pass

    def readable_parameters(self):
        pass
