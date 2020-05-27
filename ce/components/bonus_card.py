from dataclasses import dataclass
from typing import Tuple, Any


@dataclass
class BonusCard:
    ID: int
    Range1: Tuple[int, int]
    ScoreRange1: int
    Range2: Tuple[int, int]
    ScoreRange2: int
    ScoreRangeCard: int
