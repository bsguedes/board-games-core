from ce.components.board_slot import BoardSlot
from typing import List


class IndividualBoard:
    def __init__(self):
        self.champion_level: int = 0
        self.top: List[BoardSlot] = [BoardSlot() for _ in range(5)]
        self.mid: List[BoardSlot] = [BoardSlot() for _ in range(5)]
        self.bot: List[BoardSlot] = [BoardSlot() for _ in range(5)]
