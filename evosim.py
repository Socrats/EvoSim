import numpy as np
import matplotlib.pyplot as plt
import logging
from time import time

from players.players import generate_players
from games.games import NIPDGame, PGGGame, PGGiGame

logger = logging.getLogger(__name__)

N = 5
HUMAN_PLAYER = True
PMATRIX = np.array([[0.8, 0.0],
                    [1.0, 0.2]])
GENERATIONS = 1000
THRESHOLD = 100
cost = 1.0
r = 10.0
r_min = 1.0
r_max = 5.25
r_step = 0.25
nu = 1.0
runs = 1
realizations = 1
ncoop = 0.5
ninsp = 0.5

# players = generate_players(N, [['TFTPlayer', 0.8], ['RandomPlayer', 0.0], ['ParlovPlayer', 0.2]])
# game = NIPDGame(THRESHOLD, GENERATIONS, players)
# players = generate_players([['PureStrategyPlayer', 1.0]], nplayers=N, ncoop=0.5)
# game = PGGGame(players, threshold=THRESHOLD, generations=GENERATIONS, r=r, cost=cost)

players = generate_players([['PureStrategyPlayer', 1.0]], nplayers=N, ncoop=ncoop, ninsp=ninsp)
game = PGGiGame(players, threshold=THRESHOLD, generations=GENERATIONS, r=r, cost=cost, nu=nu)


if __name__ == "__main__":
    level = logging.INFO
    logging.basicConfig(level=level)

    x = np.arange(THRESHOLD, THRESHOLD + GENERATIONS)
    r_params = np.arange(r_min, r_max, r_step)
    coop_avg_run = np.empty([1, runs])
    insp_avg_run = np.empty([1, runs])
    coop_avg_real = np.empty([1, realizations])
    insp_avg_real = np.empty([1, realizations])
    coop_avg = np.arange(r_min, r_max, r_step)
    insp_avg = np.arange(r_min, r_max, r_step)
    for idx, r_param in enumerate(r_params):
        # Update r value
        logger.info("Starting simulation with r = %f", r_param)
        game.r = r_param
        for s in range(realizations):
            # Init graph
            for r in range(runs):
                logger.debug("Realization %i, run %i", s, r)
                start_time = time()
                # Init game
                game.init_game()
                game.run()
                interval = time() - start_time
                logger.debug("elapsed time: %s seconds", interval)

                # Update Avg.
                coop_avg_run[0][r] = np.mean(game.coopLevel)
                if game.__class__.__name__ == 'PGGiGame':
                    insp_avg_run[0][r] = np.mean(game.inspLevel)

                # Save and Plot results
                # plt.figure(1)
                # plt.plot(x, game.coopLevel, label='Cooperation ratio', color='g')
                # if game.__class__.__name__ == 'PGGiGame':
                #     plt.plot(x, game.inspLevel, label='Inspectors ratio', color='b')
                # plt.xlim(-1, THRESHOLD + GENERATIONS)
                # plt.ylim(-0.1, 1.2)
                # # plt.autoscale(True)
                # plt.legend()
                # plt.show()

                # Init population
                game.init_population(ncoop=ncoop, ninsp=ninsp)

            # Update the Avg.
            coop_avg_real[0][s] = np.mean(coop_avg_run)
            if game.__class__.__name__ == 'PGGiGame':
                    insp_avg_real[0][s] = np.mean(insp_avg_run)

        coop_avg[idx] = np.mean(coop_avg_real)
        insp_avg[idx] = np.mean(insp_avg_real)

    # Save and Plot results
    plt.figure(2)
    plt.plot(r_params, coop_avg, label='Cooperation ratio', color='g')
    if game.__class__.__name__ == 'PGGiGame':
        plt.plot(r_params, insp_avg, label='Inspectors ratio', color='b')
    plt.xlim(0, r_max + 1)
    plt.ylim(-0.1, 1.2)
    # plt.autoscale(True)
    plt.legend()
    plt.show()
