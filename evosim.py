import numpy as np
import matplotlib.pyplot as plt
import logging
from time import time

from players.players import generate_players
from games.games import NIPDGame, PGGGame, PGGiGame

logger = logging.getLogger(__name__)

N = 1000
HUMAN_PLAYER = True
PMATRIX = np.array([[0.8, 0.0],
                    [1.0, 0.2]])
GENERATIONS = 600
THRESHOLD = 0
cost = 1.0
r = 10.0
nu = 2.0
runs = 1
realizations = 1

# players = generate_players(N, [['TFTPlayer', 0.8], ['RandomPlayer', 0.0], ['ParlovPlayer', 0.2]])
# game = NIPDGame(THRESHOLD, GENERATIONS, players)
# players = generate_players([['PureStrategyPlayer', 1.0]], nplayers=N, ncoop=0.5)
# game = PGGGame(players, threshold=THRESHOLD, generations=GENERATIONS, r=r, cost=cost)

players = generate_players([['PureStrategyPlayer', 1.0]], nplayers=N, ncoop=0.4, ninsp=0.2)
game = PGGiGame(players, threshold=THRESHOLD, generations=GENERATIONS, r=r, cost=cost, nu=nu)


def init_population(ncoop=0.5, ninsp=0.0):
    for player in game.population.values():
        prob = np.random.uniform(0, 1)
        action = 1
        if prob < ncoop:
            action = 0
        elif prob < (ncoop + ninsp):
            action = 2
        player.init_action(action)


if __name__ == "__main__":
    start_time = time()
    level = logging.INFO
    logging.basicConfig(level=level)

    game.init_game()
    game.run()
    time = time() - start_time
    logger.info("elapsed time: %s seconds", time)

    x = np.arange(THRESHOLD, THRESHOLD + GENERATIONS)
    plt.figure(1)
    plt.plot(x, game.coopLevel, label='Cooperation ratio', color='g')
    if game.__class__.__name__ == 'PGGiGame':
        plt.plot(x, game.inspLevel, label='Inspectors ratio', color='b')
    plt.xlim(-1, THRESHOLD + GENERATIONS)
    plt.ylim(-0.1, 1.2)
    # plt.autoscale(True)
    plt.legend()
    plt.show()
