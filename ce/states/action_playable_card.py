from dataclasses import dataclass
from typing import List


@dataclass
class PlayableCard:
    ID: int
    Row: str
    CashCost: int
    TalentCost: List[str]
