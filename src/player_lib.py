import random

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
    def __init__(self, config: "GameConfig"):
        prefs = config.deck[:]
        random.shuffle(prefs)
        self.bids = {card: bid for card, bid in zip(config.deck, prefs)}

        super().__init__(config.namer.next_name())

    def _get_bid(self, card: Card) -> Bid:
        return self.bids[card]

