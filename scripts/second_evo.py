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
    # ("BREED_PAIRS", breed_lib.breed_pairs),
    # ("BREEDLESS", breed_lib.geneless_breeding),
]
ex_mutator = [
    ("MUTATE_REV", mutation_lib.reverse_mutation),
    # ("MUTATELESS", mutation_lib.no_mutation),
]
ex_gen = [15, 150]
ex_init_pop = [5, 10]
ex_seed = list(range(1, 100))
ex_mutation_degree = [0.0, 0.1, 0.2, 0.3, 0.4]


for breeder, mutator, mutation_degree, gen, init_pop, seed in itertools.product(
    ex_breeder, ex_mutator, ex_mutation_degree, ex_gen, ex_init_pop, ex_seed
):
    breeder_name, breeder_func = breeder
    mutator_name, mutator_func = mutator
    experiment_name = "/".join(
        [
            breeder_name,
            f"mutation={mutation_degree}",
            f"generations={gen}",
            f"init pop size={init_pop}",
            str(seed),
        ]
    )
    config = goofspiel.GameConfig(
        deck=[c for c in range(1, 21)],
        namer=bot_namer.NumberedNamer(),
        logger=goofspiel.GoofLogger(log_types=["FINAL_SCORE"]),
        scorer=scorer_lib.half_diff,
        breeder=breeder_func,
        mutator=mutator_func,
        mutation_degree=mutation_degree,
    )
    goofspiel.evolve_players(
        seed_players=[
            player_lib.BotPlayer(config, seed=(_ * 1000 + seed))
            for _ in range(init_pop)
        ],
        n_bots=25,
        survival_rate=10,
        config=config,
        generations=gen,
        experiment_name=experiment_name,
    )
