"""This is the main engine to run the program

This should be called from some other program."""

import logging
from typing import List, Optional, Tuple

import attr

import bot_namer
import player_lib
from shared_types import *


# TODO: Move above?
LogTypes = str


class GoofLogger(object):
    _KNOWN_LOG_TYPES: Tuple[LogTypes, ...] = (
        "ROUND",
        "BIDS",
        "PRIZES",
    )

    def __init__(
        self,
        logger: Optional[logging.Logger] = None,
        log_types: Optional[List[LogTypes]] = None,
    ):
        """This class will write messages to logger at logging level INFO if the
        message type is passed in log_types."""
        self.logger = logger
        if not self.logger:
            self.logger = logging.getLogger("default_goof_logger")
            self.logger.setLevel(logging.INFO)
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            self.logger.addHandler(console_handler)

        if log_types is None:
            self.log_types = list(self._KNOWN_LOG_TYPES)
        else:
            self.log_types = log_types[:]
        for t in self.log_types:
            if t not in self._KNOWN_LOG_TYPES:
                raise GoofErrors(f"Encountered unknown log_type: {t}")

    def round(self, number: int, bidee: Card) -> None:
        if "ROUND" not in self.log_types:
            return

        # We don't really need round number do we?
        # self.logger.info(f"Round {number}:")
        self.logger.info(f"Bid on {bidee}.")

    def bids(self, player_bids: List[Tuple[player_lib.Player, Card]]) -> None:
        if "BIDS" not in self.log_types:
            return

        for player, card in player_bids:
            self.logger.info(f"{player.name} bid {card}")

    def prizes(self, player_scores: List[Tuple[player_lib.Player, Score]]) -> None:
        if "PRIZES" not in self.log_types:
            return

        substrs = []
        for player, score in player_scores:
            if 0 == score.value():
                continue
            substrs.append(f"{player.name} wins {score.as_str()}")

        self.logger.info(", ".join(substrs))


@attr.s()
class GameConfig(object):
    deck: List[Card] = attr.ib()
    namer: bot_namer.BotNamer = attr.ib()
    logger: GoofLogger = attr.ib()
    scorer: Scorer = attr.ib()


def play_game_players(players: List[player_lib.Player], config: GameConfig) -> None:
    for player in players:
        player.new_game()

    for round_number, card in enumerate(config.deck):
        config.logger.round(round_number, card)

        player_bids: List[Tuple[player_lib.Player, Card]] = []
        for player in players:
            bid = player.get_bid(card)
            player_bids.append((player, bid))
        config.logger.bids(player_bids)

        player_scores = config.scorer(card, player_bids)
        for player, score in player_scores:
            player.add_score(score)
        config.logger.prizes(player_scores)


def play_game(n_bots: int, w_human: bool, config: GameConfig) -> None:
    players = [player_lib.BotPlayer(config) for _ in range(n_bots)]

    if w_human:
        raise NotImplementedError

    play_game_players(players, config)
