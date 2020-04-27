from tictactoe.main import TicTacToe
from random import randint


class GameFactory:
    @staticmethod
    def create_game(game_name, player_count, parameters, host_player):
        game = None
        if game_name == 'tictactoe':
            game = TicTacToe(parameters)
        game.max_players = player_count
        game.players = [host_player]
        game.match_id = randint(11111111, 99999999)
        return game
