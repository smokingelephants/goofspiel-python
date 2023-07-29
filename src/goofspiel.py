"""This is the main engine to run the program

This should be called from some other program."""

import logging
import random
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
        "RESULTS",
        "ALL_SCORES",
        "HIGH_SCORE",
        "FINAL_SCORE",
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
            # TODO: Do something smarter than attaching random number.
            self.logger = logging.getLogger(f"default_goof_logger{random.random()}")
            self.logger.setLevel(logging.INFO)
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            self.logger.addHandler(console_handler)

        if log_types is None:
            # These are the default types
            self.log_types = [
                "ROUND",
                "BIDS",
                "PRIZES",
                "RESULTS",
            ]
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

    def results(self, players: List[player_lib.Player]) -> None:
        if "RESULTS" not in self.log_types:
            return

        # Assumes players are ordered by score

        self.logger.info("=== RESULTS ===")
        for _rank, player in enumerate(players):
            rank = _rank + 1
            th = "th"
            if 1 == rank % 10:
                th = "st"
            if 2 == rank % 10:
                th = "nd"
            if 3 == rank % 10:
                th = "rd"
            rankth = f"{rank}{th}"

            self.logger.info(
                f"{player.name} got {rankth} place with {player.score.as_str()}"
            )

    def all_scores(self, generation: int, players: List[player_lib.Player]) -> None:
        if "ALL_SCORES" not in self.log_types:
            return

        all_scores = "/".join(p.score.as_str() for p in players)
        self.logger.info(f"{generation},{all_scores}")

    def high_score(self, generation: int, players: List[player_lib.Player]) -> None:
        if "HIGH_SCORE" not in self.log_types:
            return

        # Assumes players are ordered by score
        self.logger.info(f"{generation},{players[0].score.as_str()}")

    def final_score(
        self, experiment_name: Optional[str], players: List[player_lib.Player]
    ) -> None:
        if "FINAL_SCORE" not in self.log_types:
            return

        if experiment_name is None:
            experiment_name = "Unnamed experiment"

        self.logger.info(f"{experiment_name},{players[0].score.as_str()}")


@attr.s()
class GameConfig(object):
    deck: List[Card] = attr.ib()
    namer: bot_namer.BotNamer = attr.ib()
    logger: GoofLogger = attr.ib()
    scorer: Scorer = attr.ib()
    breeder: BreedFunction = attr.ib()
    mutator: MutationFunction = attr.ib()
    mutation_degree: float = attr.ib()


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

    # Rank players
    NOISE = 0.0001  # This is a hack way to break ties.
    players.sort(key=lambda p: -p.score.value() + NOISE * random.random())
    config.logger.results(players)


def evolve_players(
    seed_players: List[player_lib.BotPlayer],
    n_bots: int,
    survival_rate: int,
    generations: int,
    config: GameConfig,
    experiment_name: Optional[str] = None,
) -> None:
    players = seed_players[:]

    for gen in range(generations):
        while len(players) < n_bots:
            mom, dad = random.sample(players, 2)
            players.append(config.breeder(mom, dad, config))

        for player in players:
            config.mutator(player, config)

        if generations - 1 == gen:
            # We don't need to score them again.
            break

        play_game_players(players, config)  # This will score / sort in-place
        players = players[:survival_rate]

        config.logger.high_score(gen, players)
        config.logger.all_scores(gen, players)

    config.logger.final_score(experiment_name, players)


def play_game(n_bots: int, config: GameConfig) -> None:
    players = [player_lib.BotPlayer(config) for _ in range(n_bots)]

    # TODO: Add human player here
    raise NotImplementedError

    play_game_players(players, config)
