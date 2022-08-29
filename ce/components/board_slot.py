from ce.components.talent_tray import TalentTray
from typing import Optional
from ce.components.card import Card


class BoardSlot:
    def __init__(self):
        self.Card: Optional[Card] = None
        self.Cached: int = 0
        self.Cash: int = 0
        self.Talents: TalentTray = TalentTray()

    def is_filled(self) -> bool:
        return self.Card is not None
