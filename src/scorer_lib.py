from typing import List, Tuple

import player_lib
from shared_types import *


def half_diff(prize: Card, player_bids: List[Tuple[player_lib.Player, Bid]]) -> List[Tuple[player_lib.Player, Score]]:
    """Difference between prize rank and bid rank.  We do min to avoid double
    counting.  Negative so that more differences is worse."""
    return [(player, Score(min(prize, bid)-bid)) for player, bid in player_bids]

