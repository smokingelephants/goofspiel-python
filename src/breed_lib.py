import random
from typing import Dict, List, Tuple

import player_lib
import shared_logic
from shared_types import *


def geneless_breeding(
    mom: player_lib.BotPlayer,
    dad: player_lib.BotPlayer,
    config: "GameConfig",
    mom_perc: float = 0.5,
    dad_perc: float = 0.5,
) -> player_lib.BotPlayer:
    """For this one, just ignore parents."""
    return player_lib.BotPlayer(config)


def breed_pairs(
    mom: player_lib.BotPlayer,
    dad: player_lib.BotPlayer,
    config: "GameConfig",
    mom_perc: float = 0.5,
    dad_perc: float = 0.5,
) -> player_lib.BotPlayer:
    """We choose pairs from both parents."""
    if 1.0 != mom_perc + dad_perc:
        raise GoofErrors("Parent percentages must add to 100%")

    mom_pairs = shared_logic.pairs_from_bids(mom.bids)
    dad_pairs = shared_logic.pairs_from_bids(dad.bids)

    encountered_pairs: Set[Tuple[Card, Card]] = set()
    new_pairs: Set[Tuple[Card, Card]] = set()
    # y in less_than[x] means that x < y
    less_than = {c: set() for c in config.deck}
    # x in greater_than[y] means that x > y
    greater_than = {c: set() for c in config.deck}

    def add_pair(pair: Tuple[Card, Card]) -> None:
        nonlocal encountered_pairs
        nonlocal new_pairs
        nonlocal less_than
        nonlocal greater_than

        # This prevents repeated work
        if pair in encountered_pairs:
            return
        encountered_pairs.add(pair)

        # But we want to schedule transitives before adding `pair` because otherwise
        #  add_pair((x, y)) would get called again.
        x, y = pair
        for z in less_than[y]:
            add_pair((x, z))
        for w in greater_than[x]:
            add_pair((w, y))

        new_pairs.add(pair)
        less_than[x].add(y)
        greater_than[y].add(x)

    while len(new_pairs) < len(mom_pairs):
        # Keep adding cards
        draw_from = dad_pairs
        if random.random() < mom_perc:
            draw_from = mom_pairs

        x, y = random.choice(draw_from)
        while (x, y) in new_pairs or (y, x) in new_pairs:
            x, y = random.choice(draw_from)

        add_pair((x, y))

    bids = shared_logic.bids_from_pairs(new_pairs)
    player = player_lib.BotPlayer(config)
    player.bids = bids  # Override

    return player


def breed_prefs(
    mom: player_lib.BotPlayer,
    dad: player_lib.BotPlayer,
    config: "GameConfig",
    mom_perc: float = 0.5,
    dad_perc: float = 0.5,
) -> player_lib.BotPlayer:
    """Classic crossover technique."""
    if 1.0 != mom_perc + dad_perc:
        raise GoofErrors("Parent percentages must add to 100%")

    mom_prefs = shared_logic.prefs_from_bids(mom.bids)
    dad_prefs = shared_logic.prefs_from_bids(dad.bids)

    new_prefs = [None] * len(mom_prefs)
    used_cards = set()

    mom_size = math.floor(mom_perc * len(mom_prefs))
    if 0 == mom_size:
        return dad_prefs
    if len(mom_prefs) <= mom_size:
        return mom_prefs
    i, j = sorted(random.sample(range(len(mom_prefs)), 2))
    while j - i != mom_size:
        i, j = sorted(random.sample(range(len(mom_prefs)), 2))

    for ind in range(i, j):
        new_prefs[ind] = mom_prefs[ind]
        used_cards.add(mom_prefs[ind])

    tind = 0
    for elem in dad_prefs:
        if elem in used_cards:
            continue
        while new_prefs[tind] is not None:
            tind += 1
        new_prefs[tind] = elem

    bids = shared_logic.bids_from_prefs(new_prefs)
    player = player_lib.BotPlayer(config)
    player.bids = bids  # Override

    return player


default = breed_pairs
