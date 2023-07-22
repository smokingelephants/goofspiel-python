import sys

sys.path.append("src")

import bot_namer
import goofspiel
import scorer_lib


config = goofspiel.GameConfig(
    deck=[c for c in range(1, 4)],
    namer=bot_namer.NumberedNamer(),
    logger=goofspiel.GoofLogger(),
    scorer=scorer_lib.real_score,
)
goofspiel.play_game(n_bots=4, w_human=False, config=config)
