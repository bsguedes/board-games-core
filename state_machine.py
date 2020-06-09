from base_player import PlayerBase
from typing import List


class GameState:
    def __init__(self, name, current_player: PlayerBase, args=None):
        self.name: str = name
        self.player: PlayerBase = current_player
        self.args = args


class StateMachine:
    def __init__(self):
        self.states: List[GameState] = []
        self.index: int = 0

    def add_to_end(self, state: GameState):
        self.states.append(state)

    def add_to_next(self, state: GameState):
        self.states.insert(1, state)

    def add_states_to_next(self, states: List[GameState]):
        self.states[1:1] = states

    def add_before_first_occurrence_of(self, target_state: str, state: GameState):
        target = next(s for s in self.states if s.name == target_state)
        self.states.insert(self.states.index(target), state)

    def has_states(self) -> bool:
        return len(self.states) > 0

    def pop(self) -> GameState:
        self.index += 1
        return self.states.pop(0)

    def current_state(self) -> GameState:
        return self.states[0] if self.has_states() else None

    def remove_states(self, state_name: str, player: PlayerBase):
        count = 0
        for state in self.states:
            if state.name == state_name and state.player == player:
                count += 1
        self.states = self.states[count:]
