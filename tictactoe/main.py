from game import Game
from tictactoe.states import TicTacToePlayerState, TicTacToeFinalState
from random import sample


class TicTacToe(Game):
    def __init__(self, parameters):
        Game.__init__(self, parameters)
        self.name = 'TicTacToe'
        self.parameters = parameters
        self.X = parameters['X']
        self.Y = parameters['Y']
        self.K = parameters['K']
        self.board = None

    def setup_game(self):
        self.board = [[None for _ in range(self.X)] for _ in range(self.Y)]
        return sample(self.players, 1)[0]

    def next_player_state(self, player, current_player):
        if self.status == 'Finished':
            winner_secret = self.game_ended()
            return TicTacToeFinalState(player, winner_secret == player.secret)
        return TicTacToePlayerState(player, current_player, self.board, self.X, self.Y)

    def apply_option_on_current_state_game(self, player, option):
        x = option['X']
        y = option['Y']
        self.board[x][y] = player.secret
        if self.game_ended():
            self.status = 'Finished'
            return None
        return self.players[0] if player.secret == self.players[1].secret else self.players[1]

    def game_ended(self):
        for i in range(0, self.X - self.K + 1):
            for j in range(0, self.Y - self.K + 1):
                secret = self.check_sequence(i, j)
                if secret is not None:
                    return secret
        return None

    def check_sequence(self, x, y):
        for i in range(x, x + self.K):
            secret = self.board[i][y]
            found = True
            for j in range(y, y + self.K):
                if secret != self.board[i][j] or self.board[i][j] is None:
                    found = False
                    break
            if found:
                return secret

        for j in range(y, y + self.K):
            secret = self.board[x][j]
            found = True
            for i in range(x, x + self.K):
                if secret != self.board[i][j] or self.board[i][j] is None:
                    found = False
                    break
            if found:
                return secret

        secret = self.board[x][y]
        found = True
        for i in range(0, self.K):
            if secret != self.board[x+i][y+i] or self.board[x + i][y + i] is None:
                found = False
                break
        if found:
            return secret

        secret = self.board[x + self.K - 1][y]
        found = True
        for i in range(0, self.K):
            if secret != self.board[x + self.K - 1 - i][y + i] or self.board[x + self.K - 1 - i][y + i] is None:
                found = False
                break
        if found:
            return secret

        return None
