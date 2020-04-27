import flask
import json
from flask import request
from game_factory import GameFactory
from flask import Response
from player import Player
from random import randint


app = flask.Flask(__name__)
app.config["DEBUG"] = True

__hosted_games = dict()
__players = dict()


@app.route('/register/<string:player_name>', methods=['GET'])
def home(player_name):
    __players[player_name] = Player(player_name)
    return Response(json.dumps({}), mimetype='application/json')


@app.route('/match/new/<string:game_name>', methods=['POST'])
def new_game(game_name):
    payload = request.get_json()
    options = payload['Options']
    player_count = payload['Players']
    player = payload['Player']
    host_player = __players[player]
    host_player.secret = randint(111111111, 999999999)
    game = GameFactory.create_game(game_name, player_count, options, host_player)
    __hosted_games[game.match_id] = game
    response_payload = {
        'MatchId': game.match_id,
        'Secret': host_player.secret
    }
    return Response(json.dumps(response_payload), mimetype='application/json')


@app.route('/matches', methods=['GET'])
def matches():
    match_list = [{
        'Game': match.name,
        'Options': match.parameters,
        'MaxPlayers': match.max_players,
        'CurrentPlayers': [p.name for p in match.players],
        'Status': match.status,
        'MatchId': match.match_id
    } for match_id, match in __hosted_games.items()]
    return Response(json.dumps(match_list), mimetype='application/json')


@app.route('/match/<int:match_id>/join', methods=['POST'])
def join_match(match_id):
    payload = request.get_json()
    player = payload['Player']
    joining_player = __players[player]
    joining_player.secret = randint(111111111, 999999999)
    game = __hosted_games[match_id]
    game.players.append(joining_player)
    response_payload = {
        'MatchId': game.match_id,
        'Secret': joining_player.secret
    }
    return Response(json.dumps(response_payload), mimetype='application/json')


@app.route('/match/<int:match_id>/<int:secret>', methods=['POST'])
def start_game(match_id, secret):
    payload = request.get_json()
    player_name = payload['Player']
    game = __hosted_games[match_id]
    player = next(p for n, p in __players.items() if p.secret == secret and n == player_name)
    game.start_game()
    response_payload = {
        'Player': player.name
    }
    return Response(json.dumps(response_payload), mimetype='application/json')


@app.route('/match/<int:match_id>/state/<int:secret>', methods=['GET'])
def get_state(match_id, secret):
    game = __hosted_games[match_id]
    player = next(p for n, p in __players.items() if p.secret == secret)
    state = game.load_state_for_player(player)
    response_payload = {
        'GameStatus': game.status,
        'State': state.as_dict(),
        'CurrentPlayer': game.expecting_option_from.name,
        'Options': game.options_from_current_state if game.expecting_option_from.secret == player.secret else None
    }
    return Response(json.dumps(response_payload), mimetype='application/json')


@app.route('/match/<int:match_id>/<int:secret>/option', methods=['POST'])
def choose_option(match_id, secret):
    payload = request.get_json()
    game = __hosted_games[match_id]
    player_name = payload['Player']
    player = next(p for n, p in __players.items() if p.secret == secret and n == player_name)
    option_code = payload['OptionCode']
    valid_move = game.apply_option_on_current_state(player, option_code)
    response_payload = {
        'ValidMove': valid_move
    }
    return Response(json.dumps(response_payload), mimetype='application/json')


app.run()
