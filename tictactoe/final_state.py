from base_state import PlayerState
from tictactoe.common import code
from typing import List, Dict


class TicTacToeFinalState(PlayerState):
    def __init__(self, player, board, message):
        self.board: List[List[int]] = board
        self.message: str = message
        PlayerState.__init__(self, player, None)

    def as_dict_game(self) -> Dict:
        payload = {
            'Board': [[code(self.player.secret, x) for x in row[:]] for row in self.board],
            'Message': self.message
        }
        return payload

    def your_options_game(self) -> List[Dict]:
        pass
