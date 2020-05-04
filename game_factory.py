from tictactoe.tictactoe import TicTacToe
from ce.classificacao_etaria import ClassificacaoEtaria


def create_game(game_name, player_count, parameters, host_player):
    game = None
    if game_name == "tictactoe":
        game = TicTacToe(parameters)
    if game_name == "ce":
        game = ClassificacaoEtaria(parameters)
    game.max_players = player_count
    game.players = [host_player]
    return game
