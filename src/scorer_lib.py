from typing import List, Tuple

import player_lib
from shared_types import *


def half_diff(
    prize: Card, player_bids: List[Tuple[player_lib.Player, Bid]]
) -> List[Tuple[player_lib.Player, Score]]:
    """Difference between prize rank and bid rank.  We do min to avoid double
    counting.  Negative so that more differences is worse."""
    return [(player, Score(min(prize, bid) - bid)) for player, bid in player_bids]


def real_score(
    prize: Card, player_bids: List[Tuple[player_lib.Player, Bid]]
) -> List[Tuple[player_lib.Player, Score]]:
    max_bid = max(b for _, b in player_bids)
    num_winners = sum(1 if b == max_bid else 0 for _, b in player_bids)
    prize = Score(0, prize, num_winners)
    zero = Score(0)
    return [(p, prize if b == max_bid else zero) for p, b in player_bids]


default = real_score

