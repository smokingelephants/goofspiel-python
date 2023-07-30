import sys

sys.path.append("src")

import bot_namer
import goofspiel


config = goofspiel.GameConfig(
    deck=[c for c in range(1, 8)],
    namer=bot_namer.AliceBenjamin(),
    logger=goofspiel.GoofLogger(log_types=["RESULTS", "GUTS"]),
)
evo_config = goofspiel.EvoConfig(
    multiplicity=0,
    width=4,
    new_bots=2,
    survival_rate=2,
    generations=3,
    mutation_degree=0.2,
)
goofspiel.play_until_dead(n_bots=1, config=config, evo_config=evo_config)
