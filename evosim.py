import numpy as np
import matplotlib.pyplot as plt
import logging
from time import time

from players.players import generate_players
from games.games import NIPDGame

logger = logging.getLogger(__name__)

N = 1000
HUMAN_PLAYER = True
PMATRIX = np.array([[0.8, 0.0],
                    [1.0, 0.2]])
GENERATIONS = 1000
THRESHOLD = 0
cost = 1.0
r = 1.0


if __name__ == "__main__":
    start_time = time()
    level = logging.INFO
    logging.basicConfig(level=level)
    players = generate_players(N, [['TFTPlayer', 0.8], ['RandomPlayer', 0.0], ['ParlovPlayer', 0.2]])
    game = NIPDGame(THRESHOLD, GENERATIONS, players)
    game.run()
    time = time() - start_time
    logger.info("elapsed time: %s seconds", time)

    plt.plot(np.arange(THRESHOLD, GENERATIONS), game.coopLevel)
    plt.xlim(0, GENERATIONS)
    plt.ylim(0, 1)
    # plt.autoscale(True)
    plt.show()
