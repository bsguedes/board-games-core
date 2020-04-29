from abc import ABC, abstractmethod
from random import randint
import enum


class Game(ABC):
    def __init__(self, parameters):
        self.name = None
        self.parameters = parameters
        self.current_state_index = 0
        self.readable_parameters = None
        self.player_states = dict()
        self.match_id = str(randint(111111111, 999999999))
        self.players = []
        self.max_players = 0
        self.status = 'Lobby'
        self.options_from_current_state = dict()
        self.expecting_option_from = None

    def start_game(self):
        self.player_states = {p.secret: dict() for p in self.players}
        first_player = self.setup_game()
        for p in self.players:
            self.player_states[p.secret][0] = self.next_player_state(p, first_player)
        self.status = 'Started'
        self.expecting_option_from = first_player
        self.options_from_current_state = self.player_states[first_player.secret][0].options

    @abstractmethod
    def apply_option_on_current_state_game(self, player, option):
        pass

    @abstractmethod
    def setup_game(self):
        pass

    @abstractmethod
    def next_player_state(self, player, current_player):
        pass

    def load_state_for_player(self, player):
        return self.player_states[player.secret][self.current_state_index]

    def current_player_name(self):
        return self.expecting_option_from.name if self.expecting_option_from is not None else None

    def current_options(self, player):
        if self.expecting_option_from is not None and self.expecting_option_from.secret == player.secret:
            return self.options_from_current_state
        else:
            return None

    def apply_option_on_current_state(self, player, option_code):
        option_codes = [x['OptionCode'] for x in self.options_from_current_state]
        valid = option_code in option_codes and player.secret == self.expecting_option_from.secret
        if valid:
            option = next(p['Option'] for p in self.options_from_current_state if p['OptionCode'] == option_code)
            next_player = self.apply_option_on_current_state_game(player, option)
            n = self.current_state_index + 1
            for p in self.players:
                self.player_states[p.secret][n] = self.next_player_state(p, next_player)
            self.expecting_option_from = next_player
            options = self.player_states[next_player.secret][n].options if next_player is not None else None
            self.options_from_current_state = options
            self.current_state_index += 1
        return valid


class GameStatus(enum.Enum):
    Lobby = 1
    Started = 2
    Finished = 3
