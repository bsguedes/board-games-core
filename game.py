from abc import ABC, abstractmethod
from typing import List, Dict, Any
from base_common import rand_id_gen
from base_player import PlayerBase
from base_option import OptionBase
from state_machine import StateMachine
from base_state import PlayerState


class Game(ABC):
    def __init__(self, name: str, parameters: Dict[str, Any]):
        self.name: str = name
        self.parameters: Dict[str, Any] = parameters
        self.player_states = dict()
        self.match_id: str = rand_id_gen()
        self.players: List[PlayerBase] = []
        self.max_players: int = 0
        self.status: str = 'Lobby'
        self.options_from_current_state: List[OptionBase] = None
        self.expecting_option_from: PlayerBase = None
        self.state_machine: StateMachine = StateMachine()

    def start_game(self) -> None:
        self.player_states = {p.secret: dict() for p in self.players}
        self.setup_game()
        first_player = self.state_machine.pop().player
        for p in self.players:
            self.player_states[p.secret][0] = self.next_player_state(p, first_player)
        self.status = 'Started'
        self.expecting_option_from = first_player
        self.options_from_current_state = self.player_states[first_player.secret][0].options

    def remove_player(self, player: PlayerBase) -> None:
        if player.secret == self.players[0].secret:
            self.status = 'Cancelled'
            self.max_players = 0
            self.players = []
        else:
            self.players.remove(player)

    def can_be_listed(self, from_lobby: bool) -> bool:
        if from_lobby:
            return self.status in ['Lobby', 'Started']
        else:
            return self.status == 'Lobby' and 0 < len(self.players) < self.max_players

    def load_state_for_player(self, player: PlayerBase) -> PlayerState:
        return self.player_states[player.secret][self.state_machine.index]

    def current_player_name(self) -> str:
        return self.expecting_option_from.name if self.expecting_option_from is not None else None

    def current_options(self, player: PlayerBase):
        if self.expecting_option_from is not None and self.expecting_option_from.secret == player.secret:
            return self.options_from_current_state
        else:
            return None

    def apply_option_on_current_state(self, player: PlayerBase, option_code: OptionBase) -> bool:
        option_codes = [x.OptionCode for x in self.options_from_current_state]
        valid = option_code in option_codes and player.secret == self.expecting_option_from.secret
        if valid:
            option = next(ob.Option for ob in self.options_from_current_state if ob.OptionCode == option_code)
            self.apply_option_on_current_state_game(player, option)
            next_state = self.state_machine.pop()
            if next_state is not None:
                next_player = next_state.player
                n = self.state_machine.index
                for p in self.players:
                    self.player_states[p.secret][n] = self.next_player_state(p, next_player)
                self.expecting_option_from = next_player
                options = self.player_states[next_player.secret][n].options if next_player is not None else None
                self.options_from_current_state = options
        return valid

    @abstractmethod
    def apply_option_on_current_state_game(self, player: PlayerBase, option: Dict[str, Any]):
        pass

    @abstractmethod
    def setup_game(self):
        pass

    @abstractmethod
    def next_player_state(self, player: PlayerBase, current_player: PlayerBase):
        pass

    @abstractmethod
    def readable_parameters(self):
        pass
