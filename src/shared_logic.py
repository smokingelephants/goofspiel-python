from typing import Dict, List, Tuple

import networkx as nx

from shared_types import *


def shorthand_from_bids(bids: Dict[Card, Bid]) -> List[Bid]:
    x = [(c, b) for c, b in bids.items()]
    x.sort()
    return [xi[1] for xi in x]


def pairs_from_bids(bids: Dict[Card, Bid]) -> List[Tuple[Card, Card]]:
    """Returns (c, d) for all c, d where bids prefers d over c."""
    result = []

    for card_a, bid_a in bids.items():
        for card_b, bid_b in bids.items():
            if card_a <= card_b:
                # So that we don't double-count or self-match pairs
                continue

            if bid_a < bid_b:
                result.append((card_a, card_b))
            elif bid_b < bid_a:
                result.append((card_b, card_a))
            else:
                raise GoofErrors("This should never happen")

    return result


def bids_from_pairs(pairs: List[Tuple[Card, Card]]) -> Dict[Card, Bid]:
    graph = nx.DiGraph()
    for x, y in pairs:
        graph.add_edge(x, y)
    prefs = list(nx.topological_sort(graph))
    return bids_from_prefs(prefs)


def prefs_from_bids(bids: Dict[Card, Bid]) -> List[Card]:
    prefs = [(bid, card) for card, bid in bids.items()]
    prefs.sort()
    return [pref[1] for pref in prefs]


def bids_from_prefs(prefs: List[Card]) -> Dict[Card, Bid]:
    return {card: bid for card, bid in zip(prefs, sorted(prefs))}
