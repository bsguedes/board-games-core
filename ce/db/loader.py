import json
from ce.abilities.ability import Ability
from ce.components.bonus_card import BonusCard
from ce.components.card import Card
from ce.champions.champion import Champion, ChampionLevel
from ce.objectives.objective import Objective
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple
from collections import defaultdict


def group_by(iterable, projection) -> Dict[str, Any]:
    result = defaultdict(list)
    for item in iterable:
        result[projection(item)].append(item)
    return result


@dataclass
class Loader:
    Abilities: Dict[int, Ability]
    Cards: List[Card]
    Bonus: List[BonusCard]
    Objectives: List[Objective]
    Champions: Dict[str, List[Champion]]

    def __init__(self):
        with open('v1.json', 'r') as f:
            data = json.load(f)
        self.Abilities = {
            ab['ID']: Ability(ab['Expansion'], ab['Type'], ab['Text'])
            for ab in data['Abilities']
        }
        self.Cards = [
            Card(c['ID'], c['TopRow'], c['MidRow'], c['BotRow'], c['Cash'], c['Attribute'], c['Points'], c['CE'],
                 c['Year'], self.Abilities[c['AbilityID']], c['Cost'], c['Gender'])
            for c in data['Cards']
        ]
        self.Bonus = [
            BonusCard(bc['ID'], tuple_range(bc['Range1']), bc['ScoreRange1'], tuple_range(bc['Range2']),
                      bc['ScoreRange2'], bc['ScoreRangeCard'])
            for bc in data['Bonus']
        ]
        self.Objectives = [
            Objective(o['ID']) for o in data['Objectives']
        ]
        self.Champions = {
            channel: {champion: [ChampionLevel(b['Level'], b['AbilityName'], b['Points'], b['CashCost'],
                                               b['CardCost'], b['TalentCost'], self.Abilities[b['AbilityID']])]
                      for champion, b in obj[channel]}
            for channel, obj in group_by(data['Champions'], lambda c: c['Channel']).items()
        }


def tuple_range(rg) -> Tuple[int, int]:
    if len(rg) > 0:
        parts = rg.split('-')
        if len(parts) == 2:
            return int(parts[0]), int(parts[1])
        elif '+' in parts[0]:
            parts[0].replace('+', '')
        return int(parts[0]), 9999
    else:
        return -1, -1
