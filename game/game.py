import random
import re
from collections import Counter


class Game:
    def __init__(self):
        self.deck = []
        self.player_hand = []
        self.player_count = 0
        self.player_state = ""
        self.dealer_masked = []
        self.dealer_hand = []
        self.dealer_sum = 0
        self.dealer_state = ""
        self.natural_21 = ""
        self.winner = None
        self.suits = ["♥", "♦", "♣", "♠"]
        self.ranks = ["A", "K", "Q", "J", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

    def create_deck(self):
        self.deck = [f"{suit}{rank}" for suit in self.suits for rank in self.ranks]
        random.shuffle(self.deck)
        self.deck = self.deck[:15]

    def get_player(self):
        return self.player_hand

    def set_player(self, card):
        self.player_hand.append(card)

    def get_player_count(self):
        return self.player_count

    def set_player_count(self, count):
        self.player_count = count

    def get_player_state(self):
        return self.player_state

    def set_player_state(self, state):
        self.player_state = state

    def get_dealer(self):
        return self.dealer_hand

    def get_dealer_masked(self):
        return [self.dealer_hand[0], "✪"]

    def set_dealer(self, card):
        self.dealer_hand.append(card)

    def get_dealer_count(self):
        return self.dealer_sum

    def set_dealer_count(self, count):
        self.dealer_sum = count

    def get_dealer_state(self):
        return self.dealer_state

    def set_dealer_state(self, state):
        self.dealer_state = state

    def initialize_game(self):
        self.create_deck()
        self.set_player(self.deck.pop(0))
        self.set_dealer(self.deck.pop(0))
        self.set_player(self.deck.pop(0))
        self.set_dealer(self.deck.pop(0))

    def hand_to_ranks(self, hand):
        return "".join(c[-1] for c in hand)

    def natural_21_ranks(self, hand):
        ranks = self.hand_to_ranks(hand)
        pattern = r"^[KQJ0]A$"
        pattern1 = r"^A[KQJ0]$"
        return len(ranks) == 2 and (
            bool(re.match(pattern, ranks)) or bool(re.match(pattern1, ranks))
        )

    def natural_21_state(self):
        p_nat = self.natural_21_ranks(self.get_player())
        d_nat = self.natural_21_ranks(self.get_dealer())
        self.natural_21 = (
            "BLACKJACK PUSH"
            if p_nat and d_nat
            else (
                "BLACKJACK PLAYER WON!"
                if p_nat
                else "BLACKJACK DEALER WON!" if d_nat else ""
            )
        )
        return self.natural_21

    def sum(self, hand, is_player):
        ranks = self.hand_to_ranks(hand)
        counts = Counter(ranks)
        nums_of_ace = counts["A"]
        res = 0
        BLACKJACK_LIMIT = 21
        for rank in ranks:
            if rank in ["K", "Q", "J", "0"]:
                res += 10
            elif rank.isdigit():
                res += int(rank)
        if nums_of_ace > 0:
            for _ in range(nums_of_ace):
                if res + 11 <= BLACKJACK_LIMIT:
                    res += 11
                else:
                    res += 1
        if is_player:
            self.set_player_count(res)
            count = self.get_player_count()
            self.set_player_state(self.state(count))
        else:
            self.set_dealer_count(res)
            count = self.get_dealer_count()
            self.set_dealer_state(self.state(count))

        return res

    def state(self, count):
        state = "TWENTY ONE" if count == 21 else "BUST" if count > 21 else "UNDER 21"
        return state

    def winner_state(self):
        p = self.get_player_count()
        d = self.get_dealer_count()
        if p == d:
            self.winner = "PUSH"
        elif p > 21:
            self.winner = "PLAYER LOST"
        elif d > 21 or p > d:
            self.winner = "PLAYER WINS!"
        else:
            self.winner = "DEALER WINS!"
        return self.winner

    def hit(self, is_player):
        if is_player:
            self.set_player(self.deck.pop(0))
            self.sum(self.get_player(), True)
        else:
            count = self.sum(self.get_dealer(), False)
            while count < 17:
                self.set_dealer(self.deck.pop(0))
                count = self.sum(self.get_dealer(), False)

    def get_hit_or_stand(self, action):
        if action == "hit":
            self.hit(True)
        elif action == "stand":
            self.hit(False)
            self.sum(self.get_player(), True)
            self.winner_state()

    def serialize(self):
        return {
            "deck": self.deck,
            "player_hand": self.player_hand,
            "player_count": self.player_count,
            "player_state": self.player_state,
            "dealer_masked": self.dealer_masked,
            "dealer_hand": self.dealer_hand,
            "dealer_sum": self.dealer_sum,
            "dealer_state": self.dealer_state,
            "natural_21": self.natural_21,
            "winner": self.winner,
        }

    @classmethod
    def deserialize(cls, data):
        game = cls()
        game.deck = data["deck"]
        game.player_hand = data["player_hand"]
        game.player_count = data["player_count"]
        game.player_state = data["player_state"]
        game.dealer_masked = data["dealer_masked"]
        game.dealer_hand = data["dealer_hand"]
        game.dealer_sum = data["dealer_sum"]
        game.dealer_state = data["dealer_state"]
        game.natural_21 = data["natural_21"]
        game.winner = data["winner"]
        return game
