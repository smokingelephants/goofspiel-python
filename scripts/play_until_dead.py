import sys

sys.path.append("src")

import bot_namer
import goofspiel
import scorer_lib


config = goofspiel.GameConfig(
    deck=[c for c in range(1, 5)],
)
evo_config = goofspiel.EvoConfig()
goofspiel.play_until_dead(n_bots=2, config=config, evo_config=evo_config)
