import sys

sys.path.append("src")

import bot_namer
import goofspiel


config = goofspiel.GameConfig(
    deck=[c for c in range(1, 4)],
    namer=bot_namer.NumberedNamer(),
    logger=goofspiel.GoofLogger(),
)
goofspiel.play_game(n_bots=4, w_human=False, config=config)
