from typing import Callable, List, Tuple

import attr


# TODO: Bid and Card should kinda match...
Bid = int
# TODO: Consider making this a strong type
Card = int
Score = int

Scorer = Callable[[Card, List[Tuple["Player", Bid]]], List[Tuple["Player", Score]]]


# TOOD: Move to another file
class GoofErrors(Exception):
    """Any error that's specific to this program's code."""

    pass

