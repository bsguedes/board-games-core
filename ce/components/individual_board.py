from ce.components.board_slot import BoardSlot
from typing import List, Dict
from ce.common import COLUMN_TO_CASH


class IndividualBoard:
    def __init__(self):
        self.ChampionLevel: int = 0
        self.Rows: Dict[str, List[BoardSlot]] = {r: [BoardSlot() for _ in range(5)] for r in ROWS}

    def first_free_index(self, row: str) -> int:
        for i in range(5):
            if self.Rows[row][i].Card is None:
                return i
        return 5

    def top_action(self):
        pass

    def mid_action(self):
        pass

    def bot_action(self):
        pass

    def playable(self, row: str):
        return self.total_cash() >= COLUMN_TO_CASH[self.first_free_index(row)]

    def total_cash(self) -> int:
        return sum(sum(slot.Cash for slot in slots) for row, slots in self.Rows.items())


