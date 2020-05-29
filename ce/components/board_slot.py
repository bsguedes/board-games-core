from ce.components.talent_tray import TalentTray
from ce.components.card import Card


class BoardSlot:
    def __init__(self):
        self.Card: Card = None
        self.Cached: int = 0
        self.Cash: int = 0
        self.Talents: TalentTray = TalentTray()

    def is_filled(self) -> bool:
        return self.Card is not None
