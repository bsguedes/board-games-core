from game import Game
from ce.deck import create_deck


class ClassificacaoEtaria(Game):
    def __init__(self, parameters):
        Game.__init__(self, parameters)
        self.name = 'Classificação Etária'
        self.parameters = parameters
        self.cards = create_deck()

    def setup_game(self):
        pass

    def apply_option_on_current_state_game(self, player, option):
        pass

    def next_player_state(self, player, current_player):
        pass
