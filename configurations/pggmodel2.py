# ==============================================================================
# EvoSim
# Copyright © 2016 Elias F. Domingos. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================


import logging
from time import time

import matplotlib.pyplot as plt
import numpy as np
from games.games import PGGSocialControl
from players.players import generate_players

from evosim.network.network import regular_network

logger = logging.getLogger(__name__)

N = 5
GENERATIONS = 2000
THRESHOLD = 0
cost = 1.0
r = 1.0
r_min = 1.0
r_max = 5.125
r_step = 0.125
runs = 1
realizations = 1
freq = {'dni': 0.2, 'cni': 0.0, 'di': 0.0, 'ci': 0.8}
alpha = 0.5
gamma = 1.0
delta = 0.0
mutation = 0.0
z = N - 1
show_micro_simulations = True
store_plots = False
store_plots_dir = ""
store_data = False
store_data_dir = ""

players = generate_players([['PGGscPlayer', 1.0]], nplayers=N)
regular_network(players, z)
game = PGGSocialControl(players, threshold=THRESHOLD, generations=GENERATIONS, r=r, cost=cost, alpha=alpha, gamma=gamma,
                        delta=delta, mutation=mutation)

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

    if show_micro_simulations:
        plt.ion()  # Note this correction
        fig = plt.figure(1)
        ax = plt.axes(xlim=(-1, THRESHOLD + GENERATIONS), ylim=(-0.1, 1.2))

    for idx, r_param in enumerate(r_params):
        # Update r value
        logger.info("Starting simulation with r = %f", r_param)
        game.r = r_param
        r_start_time = time()
        for s in range(realizations):
            # Init graph
            for r in range(runs):
                logger.debug("Realization %i, run %i", s, r)
                start_time = time()
                # Init game
                game.init_game()
                # Init population
                game.init_population(dni=freq['dni'], cni=freq['cni'], di=freq['di'], ci=freq['ci'])
                game.run()
                interval = time() - start_time
                logger.debug("elapsed time: %s seconds", interval)

                # Update Avg.
                coop_avg_run[0][r] = np.mean(game.coopLevel)
                if game.__class__.__name__ == 'PGGiGame' or 'PGGiNetwork':
                    insp_avg_run[0][r] = np.mean(game.inspLevel)

                if show_micro_simulations:
                    plt.cla()
                    # Save and Plot results
                    r_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)
                    r_text.set_text('r = %.3f' % r_param)
                    ax.plot(x, game.coopLevel, label='Fraction of cooperators', color='g', lw=2)
                    if game.__class__.__name__ == 'PGGiGame' or 'PGGiNetwork':
                        ax.plot(x, game.inspLevel, label='Fraction of inspectors', color='b', lw=2)
                    ax.set_xlabel("generations")
                    ax.set_ylabel("Fraction of players")
                    ax.set_ylim(-0.1, 1.2)
                    # plt.autoscale(True)
                    ax.legend()
                    plt.show()
                    plt.pause(0.0001)

                    # Init population
                    # game.init_population(ncoop=ncoop, ninsp=ninsp)

            # Update the Avg.
            coop_avg_real[0][s] = np.mean(coop_avg_run)
            if game.__class__.__name__ == 'PGGiGame' or 'PGGiNetwork':
                insp_avg_real[0][s] = np.mean(insp_avg_run)

        coop_avg[idx] = np.mean(coop_avg_real)
        insp_avg[idx] = np.mean(insp_avg_real)
        r_interval = time() - r_start_time
        logger.info("Simulation finished: elapsed time: %s seconds", r_interval)

    if show_micro_simulations:
        plt.ioff()
    # Save and Plot results
    plt.figure(2)
    x_r = [r_param / (z + 1) for r_param in r_params]
    plt.plot(x_r, coop_avg, label='Fraction of cooperators', color='g')
    if game.__class__.__name__ == 'PGGiGame' or 'PGGiNetwork':
        plt.plot(x_r, insp_avg, label='Fraction of inspectors', color='b')
    plt.xlim(r_min / (z + 1), r_max / (z + 1))
    plt.ylim(-0.1, 1.2)
    plt.xlabel(r'$\eta = \frac{r}{z+1}$')
    plt.ylabel("Fraction of players")
    # plt.autoscale(True)
    plt.legend()
    plt.show()
