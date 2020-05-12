from base_state import PlayerState
from tictactoe.common import code
from typing import List, Dict


class TicTacToePlayerState(PlayerState):
    def __init__(self, player, current_player, board, x, y):
        self.board: List[List[int]] = board
        self.X: int = x
        self.Y: int = y
        PlayerState.__init__(self, player, current_player)

    def as_dict_game(self) -> Dict:
        payload = {
            'Board': [[code(self.player.secret, x) for x in row[:]] for row in self.board]
        }
        return payload

    def your_options_game(self) -> List[Dict]:
        options = []
        for i in range(self.X):
            for j in range(self.Y):
                if self.board[i][j] is None:
                    options.append({
                        'X': i,
                        'Y': j
                    })
        return options
