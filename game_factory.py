from tictactoe.tictactoe import TicTacToe


def create_game(game_name, player_count, parameters, host_player):
    game = None
    if game_name == "tictactoe":
        game = TicTacToe(parameters)
    game.max_players = player_count
    game.players = [host_player]
    return game
