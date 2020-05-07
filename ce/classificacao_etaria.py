from game import Game
from random import shuffle
from ce.components.deck import Deck
from ce.components.stage import Stage
from ce.components.objectives import ObjectiveBoard
from ce.components.bonus import BonusDeck
from ce.player import CEPlayer


class ClassificacaoEtaria(Game):
    def __init__(self, parameters):
        Game.__init__(self, parameters)
        self.name = 'Classificação Etária'
        self.parameters = parameters
        self.readable_parameters = 'Lorem ipsum'
        self.deck = Deck()
        self.bonus_cards = BonusDeck()
        self.objective_board = ObjectiveBoard()
        self.stage = Stage()
        self.player_objects = []
        self.corporations = shuffle(['Globo', 'Record', 'MTV', 'Band', 'SBT'])

    def setup_game(self):
        self.player_objects = [CEPlayer(player, corp) for player, corp in zip(self.players, self.corporations)]
        shuffle(self.player_objects)
        for player in self.player_objects:
            player.give_cards(self.deck.draw_cards(5))
            player.give_bonus_card(self.bonus_cards.draw_cards(2))
        return self.player_objects[0].player

    def apply_option_on_current_state_game(self, player, option):
        pass

    def next_player_state(self, player, current_player):
        pass
