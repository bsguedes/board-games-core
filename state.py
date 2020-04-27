from abc import ABC, abstractmethod
from random import randint


class PlayerState(ABC):
    def __init__(self, player, current_player):
        self.status = None
        self.player = player
        self.current_player = current_player
        self.options = self.your_options()

    def as_dict(self):
        return self.as_dict_game()

    @abstractmethod
    def as_dict_game(self):
        pass

    def your_options(self):
        if self.current_player is None or self.current_player.secret != self.player.secret:
            return None
        return {randint(111111111, 999999999): option for option in self.your_options_game()}

    @abstractmethod
    def your_options_game(self):
        pass
