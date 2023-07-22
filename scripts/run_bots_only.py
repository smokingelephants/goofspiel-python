import sys

sys.path.append("src")

import goofspiel


goofspiel.play_game(n_bots=4, w_human=False, deck=[c for c in range(1, 4)])
