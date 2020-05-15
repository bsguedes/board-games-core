import flask
import json
import os
from flask import request
from game_factory import create_game
from flask import Response
from base_player import PlayerBase
from game import Game
from typing import Dict
from base_common import to_dict
import logging


app = flask.Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

__hosted_games: Dict[str, Game] = dict()
__players: Dict[str, PlayerBase] = dict()


@app.route('/', methods=['GET'])
def home():
    return Response(json.dumps({'test': 'hello world!'}), mimetype='application/json')


@app.route('/register/<string:player_name>', methods=['GET'])
def register(player_name):
    new_player = PlayerBase(player_name)
    __players[player_name] = new_player
    response_payload = {
        'Name': player_name,
        'Secret': new_player.secret
    }
    app.logger.info(response_payload)
    return Response(json.dumps(response_payload), mimetype='application/json')


@app.route('/match/new/<string:game_name>/<string:secret>', methods=['POST'])
def new_game(game_name, secret):
    payload = request.get_json()
    options = payload['Options']
    player_count = options['MaxPlayers']
    player_name = payload['Player']
    host_player = next(p for n, p in __players.items() if p.secret == secret and n == player_name)
    game = create_game(game_name, player_count, options, host_player)
    __hosted_games[game.match_id] = game
    response_payload = {
        'MatchId': game.match_id,
        'Game': game.name,
        'Secret': host_player.secret
    }
    app.logger.info(response_payload)
    return Response(json.dumps(response_payload), mimetype='application/json')


@app.route('/matches/<int:full>', methods=['POST'])
def matches(full):
    print([(p, n.name) for p, n in __players.items()])
    payload = request.get_json()
    player_name = payload['Player']
    ping = payload['Ping']
    from_lobby = full > 0
    player = next((p for n, p in __players.items() if n == player_name), None)
    if player is not None:
        player.ping = int(ping)
    response_payload = [{
        'Game': match.name,
        'SetupSummary': match.readable_parameters(),
        'MaxPlayers': match.max_players,
        'HostPlayer': match.players[0].name,
        'CurrentPlayers': [p.name for p in match.players],
        'CurrentPings': [p.ping for p in match.players],
        'Status': match.status,
        'MatchId': match.match_id
    } for match_id, match in __hosted_games.items() if match.can_be_listed(from_lobby)]
    app.logger.info(response_payload)
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
    app.logger.info(response_payload)
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
    app.logger.info(response_payload)
    return Response(json.dumps(response_payload), mimetype='application/json')


@app.route('/match/<string:match_id>/quit/<string:secret>', methods=['POST'])
def quit_game(match_id, secret):
    payload = request.get_json()
    player_name = payload['Player']
    game = __hosted_games[match_id]
    player = next(p for n, p in __players.items() if p.secret == secret and n == player_name)
    game.remove_player(player)
    response_payload = {
        'Player': player.name
    }
    app.logger.info(response_payload)
    return Response(json.dumps(response_payload), mimetype='application/json')


@app.route('/match/<string:match_id>/state/<string:secret>', methods=['GET'])
def get_state(match_id, secret):
    game = __hosted_games[match_id]
    player = next(p for n, p in __players.items() if p.secret == secret)
    state = game.load_state_for_player(player)
    response_payload = {
        'StateNo': game.state_machine.index,
        'GameStatus': game.status,
        'State': state.as_dict(),
        'CurrentPlayer': game.current_player_name(),
        'Options': to_dict(game.current_options(player))
    }
    app.logger.info(response_payload)
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
    app.logger.info(response_payload)
    return Response(json.dumps(response_payload), mimetype='application/json')


if 'DEBUG' in os.environ and os.environ['DEBUG']:
    app.run(host='0.0.0.0')
