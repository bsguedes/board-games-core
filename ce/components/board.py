from ce.components.board_slot import BoardSlot


class Board:
    def __init__(self):
        self.champion_level = 0
        self.top = [BoardSlot() for _ in range(5)]
        self.mid = [BoardSlot() for _ in range(5)]
        self.bot = [BoardSlot() for _ in range(5)]
