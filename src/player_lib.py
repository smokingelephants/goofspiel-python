import random
from typing import Optional

from shared_types import *


class Player(object):
    def __init__(self, name: str):
        self.name = name
        self.started = False

    def new_game(self) -> None:
        self.used_bids = set()
        self.started = True
        self.score = Score(0)

    def add_score(self, score: Score) -> Bid:
        if not self.started:
            raise GoofErrors(f"Forgot to start a new game for player {self.name}")

        self.score.inc(score)

    def get_bid(self, card: Card) -> Bid:
        if not self.started:
            raise GoofErrors(f"Forgot to start a new game for player {self.name}")

        bid = self._get_bid(card)

        if bid in self.used_bids:
            raise GoofErrors(
                f"Player {self.name} can't bid {bid} because they already used it"
            )
        self.used_bids.add(bid)

        return bid

    def _get_bid(self, card: Card) -> Bid:
        raise NotImplementedError


class BotPlayer(Player):
    def __init__(self, config: "GameConfig", seed: Optional[int] = None):
        prefs = config.deck[:]
        if seed is not None:
            random.seed(seed)
        random.shuffle(prefs)
        self.bids = {card: bid for card, bid in zip(config.deck, prefs)}

        super().__init__(config.namer.next_name())

    def _get_bid(self, card: Card) -> Bid:
        return self.bids[card]


class HumanPlayer(Player):
    def __init__(self, config: "GameConfig"):
        # If advanced_bids is set, then ask for all bids before game starts
        self.advanced_bids = config.advanced_bids
        self.bids = dict()
        if self.advanced_bids:
            self.bids = {c: self._prompt_user(c) for c in config.deck}

        super().__init__("HUMAN")

    def _prompt_user(self, card: Card) -> Bid:
        return int(input(f"Enter bid for card {card}:"))

    def _get_bid(self, card: Card) -> Bid:
        if self.advanced_bids:
            return self.bids[card]
        return self._prompt_user(card)
