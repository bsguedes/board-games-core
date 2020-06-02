from ce.components.board_slot import BoardSlot
from typing import List, Dict, Tuple
from ce.common import COLUMN_TO_CASH, ROWS


class IndividualBoard:
    def __init__(self):
        self.ChampionLevel: int = 0
        self.Rows: Dict[str, List[BoardSlot]] = {r: [BoardSlot() for _ in range(5)] for r in ROWS}

    def first_free_index(self, row: str) -> int:
        for i in range(5):
            if self.Rows[row][i].Card is None:
                return i
        return 5

    def row_cost(self, row: str) -> int:
        return COLUMN_TO_CASH[self.first_free_index(row)]

    def top_action(self) -> Tuple[int, int]:
        return [(1, 0), (1, 1), (2, 0), (2, 1), (3, 0), (3, 1)][self.first_free_index(ROWS[0])]

    def mid_action(self) -> Tuple[int, int]:
        return [(2, 0), (2, 1), (3, 0), (3, 1), (4, 0), (4, 1)][self.first_free_index(ROWS[1])]

    def bot_action(self) -> Tuple[int, int]:
        return [(1, 0), (1, 1), (2, 0), (2, 1), (3, 0), (3, 1)][self.first_free_index(ROWS[2])]

    def playable(self, row: str) -> bool:
        return self.total_cash() >= self.row_cost(row)

    def total_cash(self) -> int:
        return sum(sum(slot.Cash for slot in slots) for row, slots in self.Rows.items())


