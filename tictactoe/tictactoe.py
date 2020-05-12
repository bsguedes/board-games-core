from game import Game
from base_player import PlayerBase
from tictactoe.game_state import TicTacToePlayerState
from tictactoe.final_state import TicTacToeFinalState
from random import sample
from typing import List
from state_machine import GameState


class TicTacToe(Game):
    def __init__(self, parameters):
        Game.__init__(self, 'Tic Tac Toe', parameters)
        self.X: int = parameters['X']
        self.Y: int = parameters['Y']
        self.K: int = parameters['K']
        self.board: List[List[int]] = None

    def setup_game(self):
        self.board = [[None for _ in range(self.Y)] for _ in range(self.X)]
        first_player: PlayerBase = sample(self.players, 1)[0]
        self.state_machine.add(GameState('Play', first_player))

    def readable_parameters(self):
        return '%s x %s (%s in a row)' % (self.X, self.Y, self.K)

    def next_player_state(self, player, current_player):
        if self.status == 'Finished':
            winner_secret = self.game_ended()
            return TicTacToeFinalState(player, self.board, winner_secret == player.secret)
        return TicTacToePlayerState(player, current_player, self.board, self.X, self.Y)

    def apply_option_on_current_state_game(self, player, option):
        x = option['X']
        y = option['Y']
        self.board[x][y] = player.secret
        if self.game_ended():
            self.status = 'Finished'
            self.state_machine.add(GameState('Over', player))
        else:
            next_player = self.players[0] if player.secret == self.players[1].secret else self.players[1]
            self.state_machine.add(GameState('Play', next_player))

    def game_ended(self):
        for i in range(0, self.X - self.K + 1):
            for j in range(0, self.Y - self.K + 1):
                secret = self.check_sequence(i, j)
                if secret is not None:
                    return secret
        return None

    def check_sequence(self, x, y):
        for j in range(y, y + self.K):
            secret = self.board[x][j]
            if all([self.board[i][j] == secret for i in range(x, x + self.K)]) and secret is not None:
                return secret

        for i in range(x, x + self.K):
            secret = self.board[i][y]
            if all([self.board[i][j] == secret for j in range(y, y + self.K)]) and secret is not None:
                return secret

        secret = self.board[x][y]
        if all([self.board[x + n][y + n] == secret for n in range(self.K)]) and secret is not None:
            return secret

        secret = self.board[x + self.K - 1][y]
        if all([self.board[x - n][y + n] == secret for n in range(self.K)]) and secret is not None:
            return secret

        return None
