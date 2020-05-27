from ce.components.board_slot import BoardSlot
from typing import List


class IndividualBoard:
    def __init__(self):
        self.ChampionLevel: int = 0
        self.Top: List[BoardSlot] = [BoardSlot() for _ in range(5)]
        self.Mid: List[BoardSlot] = [BoardSlot() for _ in range(5)]
        self.Bot: List[BoardSlot] = [BoardSlot() for _ in range(5)]
