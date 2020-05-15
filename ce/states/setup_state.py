from base_state import PlayerState


class SetupState(PlayerState):
    def __init__(self, player, current_player):
        self.board = board
        self.X = x
        self.Y = y
        PlayerState.__init__(self, player, current_player)

    def as_dict_game(self):
        payload = {
            'Board': [[code(self.player.secret, x) for x in row[:]] for row in self.board]
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
