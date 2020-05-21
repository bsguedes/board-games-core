from dataclasses import dataclass
from typing import Dict
from ce.abilities.ability import Ability


@dataclass
class Card:
    ID: int
    TopRow: bool
    MidRow: bool
    BotRow: bool
    MaxCash: int
    Attribute: str
    Points: int
    CE: str
    Year: int
    Ability: Ability
    Cost: Dict[str, int]
    Gender: str
