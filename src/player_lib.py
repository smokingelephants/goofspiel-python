import random
from typing import Optional

import shared_logic
from shared_types import *


class Player(object):
    def __init__(self, name: str, config: "GameConfig"):
        self.name = name
        self.started = False
        self.is_human = False
        # Keep a pointer for cloning and stuff
        self.config = config

    def new_game(self) -> None:
        self.used_bids = set()
        self.started = True
        self.score = Score(0)
        self._new_game()

    def _new_game(self) -> None:
        # Usually do nothing
        pass

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

        if bid not in self.config.deck:
            raise GoofErrors(f"Can't bid {bid}, because it's not in the deck: {self.config.deck}")

        return bid

    def _get_bid(self, card: Card) -> Bid:
        raise NotImplementedError

    def fossilize(self) -> "BotPlayer":
        """Return a robot version of this player."""
        raise NotImplementedError

    def clone(self) -> "Player":
        """Duplicate this player"""
        raise NotImplementedError


class BotPlayer(Player):
    def __init__(self, config: "GameConfig", seed: Optional[int] = None):
        prefs = config.deck[:]
        if seed is not None:
            random.seed(seed)
        random.shuffle(prefs)
        self.bids = {card: bid for card, bid in zip(config.deck, prefs)}

        super().__init__(config.namer.next_name(), config)

    def _get_bid(self, card: Card) -> Bid:
        return self.bids[card]

    def fossilize(self) -> "BotPlayer":
        # Why {self.name}, you've always been a bot.
        return self

    def clone(self) -> "BotPlayer":
        result = BotPlayer(self.config)
        result.bids = {k: v for k, v in self.bids.items()}
        return result


class HumanPlayer(Player):
    def __init__(self, config: "GameConfig"):
        # If advanced_bids is set, then ask for all bids before game starts
        self.advanced_bids = config.advanced_bids
        self.deck = config.deck[:]

        super().__init__("HUMAN", config)
        self.is_human = True

    def _new_game(self) -> None:
        self.bids = dict()
        if self.advanced_bids:
            for card in self.deck:
                self._prompt_user(card)

    def _prompt_user(self, card: Card) -> Bid:
        bid = int(input(f"Enter bid for card {card}:"))
        self.bids[card] = bid
        return bid

    def _get_bid(self, card: Card) -> Bid:
        if self.advanced_bids:
            return self.bids[card]
        return self._prompt_user(card)

    def fossilize(self) -> "BotPlayer":
        result = BotPlayer(self.config)
        result.prefs = shared_logic.prefs_from_bids(self.bids)
        return result

    def clone(self) -> "HumanPlayer":
        raise GoofErrors("Cloning humans is not yet implemented.  Try fossilizing first.")
    
