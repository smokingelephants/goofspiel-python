import random

import breed_lib
import player_lib


def no_mutation(
    player: player_lib.BotPlayer, config: "GameConfig"
) -> player_lib.BotPlayer:
    """Just always do nothing"""
    return player


def reverse_player(
    player: player_lib.BotPlayer, config: "GameConfig"
) -> player_lib.BotPlayer:
    bizarro = player_lib.BotPlayer(config)
    bizarro.bids = breed_lib.bids_from_prefs(
        breed_lib.prefs_from_bids(player.bids)[::-1]
    )
    return bizarro


def reverse_mutation(
    player: player_lib.BotPlayer, config: "GameConfig"
) -> player_lib.BotPlayer:
    if random.random() < 0.5:
        return config.breeder(
            player,
            reverse_player(player, config),
            config,
            1.0 - config.mutation_degree,
            config.mutation_degree,
        )
    # Some mutation strategies are asymmetric on mom and dad
    return config.breeder(
        reverse_player(player, config),
        player,
        config,
        config.mutation_degree,
        1.0 - config.mutation_degree,
    )
