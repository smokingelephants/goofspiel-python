import sys

sys.path.append("src")

import bot_namer
import goofspiel


config = goofspiel.GameConfig(
    deck=[c for c in range(1, 8)],
    namer=bot_namer.AliceBenjamin(),
)
evo_config = goofspiel.EvoConfig(
    multiplicity=0,
    width=10,
    new_bots=2,
    survival_rate=5,
    generations=2,
    mutation_degree=0.1,
)
goofspiel.play_until_dead(n_bots=1, config=config, evo_config=evo_config)
