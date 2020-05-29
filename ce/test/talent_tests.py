import unittest
from ce.test.factory.factories import card_factory, talent_tray_factory


class TalentTrayTest(unittest.TestCase):

    def test_card_cost_1(self):
        cost = {"X1": 1, "X2": 1, "X": 1}
        card = card_factory(cost)
        talent_tray = talent_tray_factory(2, 1, 1, 0, 0)
        options = talent_tray.payment_methods(card)
        self.assertEqual(2, len(options))

    def test_card_cost_2(self):
        cost = {"X1": 0.25, "X2": 0.25}
        card = card_factory(cost)
        talent_tray = talent_tray_factory(0, 1, 0, 0, 1)
        options = talent_tray.payment_methods(card)
        self.assertEqual(1, len(options))

    def test_card_cost_3(self):
        cost = {"X1": 0.25, "X2": 0.25}
        card = card_factory(cost)
        talent_tray = talent_tray_factory(0, 0, 1, 1, 1)
        options = talent_tray.payment_methods(card)
        self.assertEqual(3, len(options))

    def test_card_cost_4(self):
        cost = {"X1": 1, "X2": 1}
        card = card_factory(cost)
        talent_tray = talent_tray_factory(0, 0, 1, 1, 1)
        options = talent_tray.payment_methods(card)
        self.assertEqual(0, len(options))

    def test_card_cost_5(self):
        cost = {"X": 3}
        card = card_factory(cost)
        talent_tray = talent_tray_factory(0, 1, 1, 1, 1)
        options = talent_tray.payment_methods(card)
        self.assertEqual(4, len(options))

    def test_card_cost_6(self):
        cost = {"X1": 2, "X": 1}
        card = card_factory(cost)
        talent_tray = talent_tray_factory(1, 3, 1, 2, 1)
        options = talent_tray.payment_methods(card)
        self.assertEqual(19, len(options))

    def test_card_cost_7(self):
        cost = {"X1": 1}
        card = card_factory(cost)
        talent_tray = talent_tray_factory(1, 1, 1, 0, 0)
        options = talent_tray.payment_methods(card)
        self.assertEqual(2, len(options))

    def test_card_cost_8(self):
        cost = {"X1": 0.25, "X2": 0.25}
        card = card_factory(cost)
        talent_tray = talent_tray_factory(0, 1, 1, 0, 1)
        options = talent_tray.payment_methods(card)
        self.assertEqual(2, len(options))


if __name__ == '__main__':
    unittest.main()
