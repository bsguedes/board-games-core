from state import PlayerState
from tictactoe.common import code


class TicTacToeFinalState(PlayerState):
    def __init__(self, player, board, is_winner):
        self.player = player
        self.board = board
        self.is_winner = is_winner
        PlayerState.__init__(self, player, None)

    def as_dict_game(self):
        payload = {
            'Board': [[code(self.player.secret, x) for x in row[:]] for row in self.board],
            'Message': 'Winner' if self.is_winner else 'Loser'
        }
        return payload

    def your_options_game(self):
        return None
