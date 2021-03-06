from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from base_option import OptionBase
from base_player import PlayerBase


class PlayerState(ABC):
    def __init__(self, player: PlayerBase, current_player: Optional[PlayerBase]):
        self.status = None
        self.player: PlayerBase = player
        self.current_player: PlayerBase = current_player
        self.options: List[OptionBase] = self.your_options()

    def as_dict(self, state_name: str) -> Dict:
        state_contents = {'StateName': state_name}
        state_contents.update(self.as_dict_game())
        return state_contents

    def your_options(self):
        if self.current_player is None or self.current_player.secret != self.player.secret:
            return None
        return [OptionBase(option) for option in self.your_options_game()]

    @abstractmethod
    def as_dict_game(self) -> Dict:
        pass

    @abstractmethod
    def your_options_game(self) -> List[Dict]:
        pass
