from dataclasses import dataclass
from typing import List, Dict
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
    Cost: Dict[str, float]
    Gender: str
    CurrentCash: int = 0

    def cost_type(self) -> str:
        if all(c == 0 for t, c in self.Cost.items()):
            return 'None'
        elif any(0 < c < 1 for t, c in self.Cost.items()):
            return 'OR'
        else:
            return 'AND'

    def can_be_paid_with(self, player_talents: List[str]) -> bool:
        talents = [t for t in player_talents]
        cost_type = self.cost_type()
        if cost_type == 'OR':
            card_cost = [t for t, c in self.Cost.items() if 0 < c < 1]
            return (len(talents) == 1 and talents[0] in card_cost) or \
                   (len(talents) == 2 and talents[0] not in card_cost and talents[1] not in card_cost)
        elif cost_type == 'AND':
            card_cost = [i for s in [[t] * int(c) for t, c in self.Cost.items()] for i in s]
            commons = []
            for talent in talents:
                if talent in card_cost:
                    card_cost.remove(talent)
                    commons.append(talent)
            for talent in commons:
                talents.remove(talent)
            if any(t in card_cost for t in talents):
                return False
            else:
                joker_count = sum([int(c) for t, c in self.Cost.items() if t == 'X'])
                return 2 * len(card_cost) - joker_count == len(talents)
        else:
            return True

