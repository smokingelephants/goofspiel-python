"""This is the main engine to run the program

This should be called from some other program."""

import random
from typing import List, Tuple

# TODO: Bid and Card should kinda match...
Bid = int
# TODO: Consider making this a strong type
Card = int


class Player(object):
    def __init__(self, name: str):
        self.name = name

    def get_bid(self, card: Card) -> Bid:
        raise NotImplementedError


class BotPlayer(Player):
    def __init__(self, cards: List[Card]):
        prefs = cards[:]
        random.shuffle(prefs)
        self.bids = {card: bid for card, bid in zip(cards, prefs)}

        super().__init__("Some bot")

    def get_bid(self, card: Card) -> Bid:
        return self.bids[card]


def play_game_players(players: List[Player], deck: List[Card]) -> None:
    for card in deck:
        player_bids: List[Tuple[Player, Card]] = []
        for player in players:
            bid = player.get_bid(card)
            player_bids.append((player, bid))

        # TODO: Add scoring part

        # TODO: Pass logger
        print(player_bids)


def play_game(n_bots: int, w_human: bool, deck: List[Card]) -> None:
    players = [BotPlayer(deck) for _ in range(n_bots)]

    if w_human:
        raise NotImplementedError

    play_game_players(players, deck)
