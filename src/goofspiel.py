"""This is the main engine to run the program

This should be called from some other program."""

import random
from typing import List, Tuple

import attr

# TODO: Bid and Card should kinda match...
Bid = int
# TODO: Consider making this a strong type
Card = int


class Player(object):
    def __init__(self, name: str):
        self.name = name

    def get_bid(self, card: Card) -> Bid:
        raise NotImplementedError


@attr.s()
class GameConfig(object):
    deck: List[Card] = attr.ib()


class BotPlayer(Player):
    def __init__(self, cards: List[Card]):
        prefs = cards[:]
        random.shuffle(prefs)
        self.bids = {card: bid for card, bid in zip(cards, prefs)}

        super().__init__("Some bot")

    def get_bid(self, card: Card) -> Bid:
        return self.bids[card]


def play_game_players(players: List[Player], config: GameConfig) -> None:
    for card in config.deck:
        player_bids: List[Tuple[Player, Card]] = []
        for player in players:
            bid = player.get_bid(card)
            player_bids.append((player, bid))

        # TODO: Add scoring part

        # TODO: Pass logger
        print(player_bids)


def play_game(n_bots: int, w_human: bool, config: GameConfig) -> None:
    players = [BotPlayer(config.deck) for _ in range(n_bots)]

    if w_human:
        raise NotImplementedError

    play_game_players(players, config)
