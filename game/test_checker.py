import unittest

from game import Game


class TestgameSum(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def test_sum(self):
        ranks0 = ["♥A", "♣3", "♥8", "♣6"]
        ranks1 = ["♥8", "♣4", "♥4", "♣A"]
        ranks2 = ["♥A", "♣8"]
        ranks3 = ["♥10", "♣8"]
        ranks4 = ["♥A", "♣6"]
        ranks5 = ["♥A", "♣2", "♣3", "♥5", "♣2"]
        ranks6 = ["♥A", "♣Q"]
        ranks7 = ["♥K", "♣A"]
        ranks8 = ["♥A", "♣A", "♥4", "♣5"]
        ranks9 = ["♠J", "♦2", "♥A", "♣7"]
        ranks10 = ["♥8", "♣4", "♥A"]
        ranks11 = ["♥8", "♥A", "♣A", "♠A"]
        ranks12 = ["♥8", "♥A", "♣A", "♠A", "♦A"]
        ranks13 = ["♥A", "♣A", "♠A"]
        ranks14 = ["♥A", "♥5", "♣A", "♠A"]
        ranks15 = ["♥A", "♣A", "♠A", "♦A"]
        ranks16 = ["♥A", "♣A", "♥5", "♠A"]

        self.assertEqual(18, self.game.sum(ranks0, True))
        self.assertEqual(17, self.game.sum(ranks1, True))
        self.assertEqual(19, self.game.sum(ranks2, True))
        self.assertEqual(18, self.game.sum(ranks3, True))
        self.assertEqual(17, self.game.sum(ranks4, False))
        self.assertEqual(13, self.game.sum(ranks5, True))
        self.assertEqual(21, self.game.sum(ranks6, True))
        self.assertEqual(21, self.game.sum(ranks7, True))
        self.assertEqual(21, self.game.sum(ranks6, False))
        self.assertEqual(21, self.game.sum(ranks8, True))
        self.assertEqual(20, self.game.sum(ranks9, False))
        self.assertEqual(13, self.game.sum(ranks10, False))
        self.assertEqual(21, self.game.sum(ranks11, False))
        self.assertEqual(22, self.game.sum(ranks12, False))
        self.assertEqual(21, self.game.sum(ranks11, True))
        self.assertEqual(22, self.game.sum(ranks12, True))
        self.assertEqual(13, self.game.sum(ranks13, False))
        self.assertEqual(14, self.game.sum(ranks15, False))
        self.assertEqual(13, self.game.sum(ranks13, True))
        self.assertEqual(14, self.game.sum(ranks15, True))
        self.assertEqual(18, self.game.sum(ranks14, True))
        self.assertEqual(18, self.game.sum(ranks14, False))
        self.assertEqual(18, self.game.sum(ranks16, True))
        self.assertEqual(18, self.game.sum(ranks16, False))

    def test_blackjack(self):
        ranks0 = ["♥A", "♣10"]
        ranksJ = ["♦A", "♥J"]
        ranksQ = ["♣A", "♠Q"]
        ranksK = ["♠A", "♣K"]
        ranksA = ["♥10", "♣A"]
        ranks = ["♥10", "♣K"]
        ranks3 = ["♥A", "♣3"]
        ranks6 = ["♥6", "♣A"]

        self.assertEqual(21, self.game.sum(ranks0, True))
        self.assertEqual(21, self.game.sum(ranksJ, True))
        self.assertEqual(21, self.game.sum(ranksQ, True))
        self.assertEqual(21, self.game.sum(ranksK, True))
        self.assertEqual(21, self.game.sum(ranksA, True))
        self.assertEqual(21, self.game.sum(ranks0, False))
        self.assertEqual(21, self.game.sum(ranksJ, False))
        self.assertEqual(21, self.game.sum(ranksQ, False))
        self.assertEqual(21, self.game.sum(ranksK, False))
        self.assertEqual(21, self.game.sum(ranksA, False))
        self.assertEqual(20, self.game.sum(ranks, True))
        self.assertEqual(14, self.game.sum(ranks3, True))
        self.assertEqual(17, self.game.sum(ranks6, True))

    def test_sum_player_no_aces(self):
        hand = ["♥10", "♦5", "♣3"]
        result = self.game.sum(hand, True)
        self.assertEqual(result, 18)
        self.assertEqual(self.game.get_player_count(), 18)

    def test_sum_dealer_no_aces(self):
        hand = ["♠K", "♥7", "♦2"]
        result = self.game.sum(hand, False)
        self.assertEqual(result, 19)
        self.assertEqual(self.game.get_dealer_count(), 19)

    def test_sum_player_one_ace_under_21(self):
        hand = ["♥A", "♦10"]
        result = self.game.sum(hand, True)
        self.assertEqual(result, 21)
        self.assertEqual(self.game.get_player_count(), 21)

    def test_sum_player_one_ace_over_21(self):
        hand = ["♥A", "♦10", "♣9"]
        result = self.game.sum(hand, True)
        self.assertEqual(result, 20)
        self.assertEqual(self.game.get_player_count(), 20)

    def test_sum_dealer_one_ace_under_21(self):
        hand = ["♥A", "♦10"]
        result = self.game.sum(hand, False)
        self.assertEqual(result, 21)
        self.assertEqual(self.game.get_dealer_count(), 21)

    def test_sum_dealer_one_ace_over_21(self):
        hand = ["♥A", "♦10", "♣9"]
        result = self.game.sum(hand, False)
        self.assertEqual(result, 20)
        self.assertEqual(self.game.get_dealer_count(), 20)

    def test_sum_player_multiple_aces(self):
        hand = ["♥A", "♦A", "♣9"]
        result = self.game.sum(hand, True)
        self.assertEqual(result, 21)
        self.assertEqual(self.game.get_player_count(), 21)

    def test_sum_dealer_multiple_aces(self):
        hand = ["♥A", "♦A", "♣9"]
        result = self.game.sum(hand, False)
        self.assertEqual(result, 21)
        self.assertEqual(self.game.get_dealer_count(), 21)

    def test_sum_dealer_ace_near_17(self):
        hand = ["10", "6", "A"]
        result = self.game.sum(hand, False)
        self.assertEqual(result, 17)
        self.assertEqual(self.game.get_dealer_count(), 17)


if __name__ == "__main__":
    unittest.main()
