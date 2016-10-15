################
# evoSim
# Copyright © 2016 Elias F. Domingos
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#################


import numpy as np
import logging

from players.players import generate_players
from games.games import NIPDGame, PGGGame, PGGiGame, PGGiNetwork
from network.network import regular_network, scale_free_network

logger = logging.getLogger(__name__)

level = logging.INFO
logging.basicConfig(level=level)

N = 100
HUMAN_PLAYER = False
PMATRIX = np.array([[0.8, 0.0],
                    [1.0, 0.2]])
GENERATIONS = 1000
THRESHOLD = 0
cost = 1.0
# r = 3
r_min = 1.0
r_max = 5.25
r_step = 0.25
nu = 1.0
runs = 1
realizations = 1
ncoop = 0.5
ninsp = 0.0
z = 4
show_micro_simulations = True
store_plots = False
store_plots_dir = ""
store_data = False
store_data_dir = ""

# players = generate_players(N, [['TFTPlayer', 0.8], ['RandomPlayer', 0.0], ['ParlovPlayer', 0.2]])
# game = NIPDGame(THRESHOLD, GENERATIONS, players)
# players = generate_players([['PureStrategyPlayer', 1.0]], nplayers=N, ncoop=0.5)
# game = PGGGame(players, threshold=THRESHOLD, generations=GENERATIONS, r=r, cost=cost)

# players = generate_players([['PureStrategyPlayer', 1.0]], nplayers=N, ncoop=ncoop, ninsp=ninsp)
# game = PGGiGame(players, threshold=THRESHOLD, generations=GENERATIONS, r=r, cost=cost, nu=nu)

players = generate_players([['PGGiPlayer', 1.0]], nplayers=N)
# players = generate_players([['BMPlayer', 0.3], ['PGGiPlayer', 0.7]], nplayers=N)
# players = generate_players([['PureStrategyPlayer', 1.0]], nplayers=N)
# regular_network(players, z)
scale_free_network(players, m0=2)
game = PGGiNetwork(players, threshold=THRESHOLD, generations=GENERATIONS, cost=cost, nu=nu)
# game = PGGGame(players, threshold=THRESHOLD, generations=GENERATIONS, cost=cost)

# Define a simulation object

# simulation.run()
