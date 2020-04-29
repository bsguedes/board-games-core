from state import PlayerState


class TicTacToeFinalState(PlayerState):
    def __init__(self, player, board, is_winner):
        self.player = player
        self.board = board
        self.is_winner = is_winner
        PlayerState.__init__(self, player, None)

    def as_dict_game(self):
        payload = {
            'Board': [[TicTacToePlayerState.code(self.player.secret, x) for x in row[:]] for row in self.board],
            'Message': 'Winner' if self.is_winner else 'Loser'
        }
        return payload

    def your_options_game(self):
        return None


class TicTacToePlayerState(PlayerState):
    def __init__(self, player, current_player, board, x, y):
        self.board = board
        self.X = x
        self.Y = y
        PlayerState.__init__(self, player, current_player)

    def as_dict_game(self):
        payload = {
            'Board': [[TicTacToePlayerState.code(self.player.secret, x) for x in row[:]] for row in self.board]
        }
        return payload

    def your_options_game(self):
        options = []
        for i in range(self.X):
            for j in range(self.Y):
                if self.board[i][j] is None:
                    options.append({
                        'X': i,
                        'Y': j
                    })
        return options

    @staticmethod
    def code(secret, value):
        return None if value is None else secret == value
