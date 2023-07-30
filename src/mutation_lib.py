import random

import player_lib
import shared_logic


def no_mutation(
    player: player_lib.BotPlayer, mutation_degree: float, config: "GameConfig"
) -> player_lib.BotPlayer:
    """Just always do nothing"""
    return player


def reverse_player(
    player: player_lib.BotPlayer, config: "GameConfig"
) -> player_lib.BotPlayer:
    bizarro = player_lib.BotPlayer(config)
    bizarro.bids = shared_logic.bids_from_prefs(
        shared_logic.prefs_from_bids(player.bids)[::-1]
    )
    return bizarro


def reverse_mutation(
    player: player_lib.BotPlayer, mutation_degree:float, config: "GameConfig"
) -> player_lib.BotPlayer:
    if random.random() < 0.5:
        return config.breeder(
            player,
            reverse_player(player, config),
            config,
            1.0 - mutation_degree,
            mutation_degree,
        )
    # Some mutation strategies are asymmetric on mom and dad
    return config.breeder(
        reverse_player(player, config),
        player,
        config,
        mutation_degree,
        1.0 - mutation_degree,
    )


default = reverse_mutation
