import sys

sys.path.append("src")

import bot_namer
import goofspiel
import scorer_lib


config = goofspiel.GameConfig(
    deck=[c for c in range(1, 5)],
)
goofspiel.play_game(n_bots=2, config=config)
