import unittest
from base_player import PlayerBase
from ce.components.objective_board import ObjectiveBoard
from ce.components.deck import Deck
from ce.components.bonus_deck import BonusDeck
from ce.components.card import Card
from ce.components.bonus_card import BonusCard
from ce.abilities.ability import Ability
from ce.components.stage import Stage
from ce.champions.champion import Champion
from ce.states.ce_choose_resources import CEChooseResources
from ce.player import CEPlayer


class CEChooseResourcesTest(unittest.TestCase):
    def setUp(self):
        p = PlayerBase('test')
        ce_player = CEPlayer(p, Champion('Test', []))
        deck = Deck([Card(i, True, True, True, 1, 'Test', 1, 'L', 1990,
                          Ability('a', 'b', 'c'), {}, 'M') for i in range(10)])
        bonus_deck = BonusDeck([BonusCard(i, (-1, -1), 0, (-1, -1), 0, 2) for i in range(10)])
        ce_player.give_cards(deck.draw_cards(5))
        ce_player.give_bonus_cards(bonus_deck.draw_cards(2))
        self.state = CEChooseResources(p, p, deck, 2, ObjectiveBoard([]), Stage(), [ce_player])

    def test_your_options_game(self):
        options = self.state.your_options_game()
        self.assertEqual(504, len(options))


if __name__ == '__main__':
    unittest.main()
