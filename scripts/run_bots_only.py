import sys

sys.path.append("src")

import goofspiel


config = goofspiel.GameConfig(deck=[c for c in range(1, 4)])
goofspiel.play_game(n_bots=4, w_human=False, config=config)
