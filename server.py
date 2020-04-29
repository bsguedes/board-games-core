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
def register(player_name):
    secret = str(randint(111111111, 999999999))
    __players[player_name] = Player(player_name, secret)
    response_payload = {
        'Name': player_name,
        'Secret': secret
    }
    print(response_payload)
    return Response(json.dumps(response_payload), mimetype='application/json')


@app.route('/match/new/<string:game_name>/<string:secret>', methods=['POST'])
def new_game(game_name, secret):
    payload = request.get_json()
    options = payload['Options']
    player_count = options['MaxPlayers']
    player_name = payload['Player']
    host_player = next(p for n, p in __players.items() if p.secret == secret and n == player_name)
    game = GameFactory.create_game(game_name, player_count, options, host_player)
    __hosted_games[game.match_id] = game
    response_payload = {
        'MatchId': game.match_id,
        'Secret': host_player.secret
    }
    print(response_payload)
    return Response(json.dumps(response_payload), mimetype='application/json')


@app.route('/matches', methods=['GET'])
def matches():
    response_payload = [{
        'Game': match.name,
        'SetupSummary': match.readable_parameters,
        'MaxPlayers': match.max_players,
        'HostPlayer': match.players[0].name,
        'CurrentPlayers': [p.name for p in match.players],
        'Status': match.status,
        'MatchId': match.match_id
    } for match_id, match in __hosted_games.items()]
    print(response_payload)
    return Response(json.dumps(response_payload), mimetype='application/json')


@app.route('/match/<string:match_id>/join', methods=['POST'])
def join_match(match_id):
    payload = request.get_json()
    player = payload['Player']
    joining_player = __players[player]
    game = __hosted_games[match_id]
    game.players.append(joining_player)
    response_payload = {
        'MatchId': game.match_id,
        'Secret': joining_player.secret
    }
    print(response_payload)
    return Response(json.dumps(response_payload), mimetype='application/json')


@app.route('/match/<string:match_id>/start/<string:secret>', methods=['POST'])
def start_game(match_id, secret):
    payload = request.get_json()
    player_name = payload['Player']
    game = __hosted_games[match_id]
    player = next(p for n, p in __players.items() if p.secret == secret and n == player_name)
    game.start_game()
    response_payload = {
        'Player': player.name
    }
    print(response_payload)
    return Response(json.dumps(response_payload), mimetype='application/json')


@app.route('/match/<string:match_id>/state/<string:secret>', methods=['GET'])
def get_state(match_id, secret):
    game = __hosted_games[match_id]
    player = next(p for n, p in __players.items() if p.secret == secret)
    state = game.load_state_for_player(player)
    response_payload = {
        'StateNo': game.current_state_index,
        'GameStatus': game.status,
        'State': state.as_dict(),
        'CurrentPlayer': game.current_player_name(),
        'Options': game.current_options(player)
    }
    print(response_payload)
    return Response(json.dumps(response_payload), mimetype='application/json')


@app.route('/match/<string:match_id>/option/<string:secret>', methods=['POST'])
def choose_option(match_id, secret):
    payload = request.get_json()
    print(payload)
    game = __hosted_games[match_id]
    player_name = payload['Player']
    player = next(p for n, p in __players.items() if p.secret == secret and n == player_name)
    option_code = payload['OptionCode']
    valid_move = game.apply_option_on_current_state(player, option_code)
    response_payload = {
        'Player': player.name,
        'ValidMove': valid_move
    }
    print(response_payload)
    return Response(json.dumps(response_payload), mimetype='application/json')


app.run()
