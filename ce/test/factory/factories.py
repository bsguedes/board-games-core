from ce.components.card import Card
from ce.abilities.ability import Ability
from ce.components.talent_tray import TalentTray


def card_factory(cost=None):
    return Card(1,
                True,
                True,
                True,
                1,
                'Test',
                1,
                'L',
                1990,
                Ability('a', 'b', 'c'),
                {} if cost is None else cost,
                'M')


def talent_tray_factory(x1=0, x2=0, x3=0, x4=0, x5=0):
    return TalentTray(x1, x2, x3, x4, x5)
