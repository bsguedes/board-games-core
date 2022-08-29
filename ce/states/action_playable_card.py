from dataclasses import dataclass
from typing import List, Optional


@dataclass
class PlayableCard:
    ID: int
    ValidRows: List[str]
    CashCost: List[int]
    TalentCost: Optional[List[str]]
