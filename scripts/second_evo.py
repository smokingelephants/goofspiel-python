import itertools
import sys

sys.path.append("src")

import bot_namer
import breed_lib
import goofspiel
import mutation_lib
import player_lib
import scorer_lib


ex_breeder = [
    ("BREED_PREFS", breed_lib.breed_prefs),
    ("BREED_PAIRS", breed_lib.breed_pairs),
    ("BREEDLESS", breed_lib.geneless_breeding),
]
ex_gen = [20, 200]
ex_init_pop = [5, 10]
ex_seed = list(range(1, 50))


for breeder, gen, init_pop, seed in itertools.product(ex_breeder, ex_gen, ex_init_pop, ex_seed):
    breeder_name, breeder_func = breeder
    experiment_name = f"{breeder_name}/generations={gen}/init pop size={init_pop}/{seed}"
    config = goofspiel.GameConfig(
        deck=[c for c in range(1, 21)],
        namer=bot_namer.NumberedNamer(),
        logger=goofspiel.GoofLogger(log_types=["FINAL_SCORE"]),
        scorer=scorer_lib.half_diff,
        breeder=breeder_func,
        mutator=mutation_lib.no_mutation,
        mutation_degree=0.0,
    )
    goofspiel.evolve_players(
        seed_players=[player_lib.BotPlayer(config, seed=(_*1000+seed)) for _ in range(init_pop)],
        n_bots=25,
        survival_rate=10,
        config=config,
        generations=gen,
        experiment_name=experiment_name,
    )

