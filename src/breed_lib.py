import player_lib


def geneless_breeding(
    mom: player_lib.BotPlayer, dad: player_lib.BotPlayer, config: "GameConfig"
) -> player_lib.BotPlayer:
    """For this one, just ignore parents."""
    return player_lib.BotPlayer(config)
