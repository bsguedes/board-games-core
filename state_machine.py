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

    def add(self, state: GameState):
        self.states.append(state)

    def has_states(self) -> bool:
        return len(self.states) > 0

    def pop(self) -> GameState:
        self.index += 1
        return self.states.pop(0)

    def current_state(self) -> GameState:
        return self.states[0] if self.has_states() else None
