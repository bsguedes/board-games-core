from dataclasses import dataclass
from typing import List, Dict
from ce.abilities.ability import Ability


@dataclass
class ChampionLevel:
    Level: int
    LevelName: str
    Points: int
    CashCost: int
    CardCost: int
    TokenCost: Dict[str, int]
    Ability: Ability


@dataclass
class Champion:
    Name: str
    Levels: List[ChampionLevel]


@dataclass
class Channel:
    Name: str
    Champions: List[Champion]
