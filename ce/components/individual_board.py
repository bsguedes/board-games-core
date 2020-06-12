from ce.components.board_slot import BoardSlot
from typing import List, Dict, Tuple, Optional
from ce.common import COLUMN_TO_CASH, ROWS

ROW_SIZE = 5


class IndividualBoard:
    def __init__(self):
        self.ChampionLevel: int = 0
        self.TopRow: List[BoardSlot] = [BoardSlot() for _ in range(ROW_SIZE)]
        self.MidRow: List[BoardSlot] = [BoardSlot() for _ in range(ROW_SIZE)]
        self.BotRow: List[BoardSlot] = [BoardSlot() for _ in range(ROW_SIZE)]

    def add_card_to_row(self, card_id: int, row: str):
        index = self.first_free_index(row)
        slot: BoardSlot = self.rows(row)[index]
        slot.Card = card_id

    def first_free_index(self, row: str) -> int:
        for i in range(ROW_SIZE):
            if self.rows(row)[i].Card is None:
                return i
        return ROW_SIZE

    def rows(self, row: str) -> List[BoardSlot]:
        if row == 'Top':
            return self.TopRow
        elif row == 'Mid':
            return self.MidRow
        elif row == 'Bot':
            return self.BotRow

    def row_cost(self, row: str) -> int:
        return COLUMN_TO_CASH[self.first_free_index(row)]

    def top_action(self) -> Tuple[int, int]:
        return [(1, 0), (1, 1), (2, 0), (2, 1), (3, 0), (3, 1)][self.first_free_index(ROWS[0])]

    def mid_action(self) -> Tuple[int, int]:
        return [(2, 0), (2, 1), (3, 0), (3, 1), (4, 0), (4, 1)][self.first_free_index(ROWS[1])]

    def bot_action(self) -> Tuple[int, int]:
        return [(1, 0), (1, 1), (2, 0), (2, 1), (3, 0), (3, 1)][self.first_free_index(ROWS[2])]

    def playable(self, row: str) -> bool:
        fits_in_row = len([s for s in self.rows(row) if s.Card is not None]) < ROW_SIZE
        can_pay_slot = self.total_cash() >= self.row_cost(row)
        return fits_in_row and can_pay_slot

    def cash_in_row(self, row: str) -> int:
        return sum(slot.Cash for slot in self.rows(row))

    def total_cash(self) -> int:
        return self.cash_in_row('Top') + self.cash_in_row('Mid') + self.cash_in_row('Bot')

    def cards_with_cash(self) -> List[Optional[int]]:
        return [slot.Card for row in ROWS for slot in self.rows(row) if slot.Cash > 0]

    def cards_in_board(self) -> List[Optional[int]]:
        return [slot.Card for row in ROWS for slot in self.rows(row)]
