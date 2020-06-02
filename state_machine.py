from base_player import PlayerBase
from typing import List


class GameState:
    def __init__(self, name, current_player: PlayerBase):
        self.name: str = name
        self.player: PlayerBase = current_player


class StateMachine:
    def __init__(self):
        self.states: List[GameState] = []
        self.index: int = -1

    def add_to_end(self, state: GameState):
        self.states.append(state)

    def add_to_next(self, state: GameState):
        self.states.insert(0, state)

    def add_states_to_next(self, states: List[GameState]):
        self.states[0:0] = states

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
