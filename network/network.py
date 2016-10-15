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


from numpy import random
import logging

logger = logging.getLogger(__name__)


class AbstractNetwork:
    def __init__(self):
        pass


class GridNetwork(AbstractNetwork):
    pass


class RegularNetwork(AbstractNetwork):
    pass


class RandomNetwork(AbstractNetwork):
    pass


class ScaleFreeNetwork(AbstractNetwork):
    pass


class SmallWorldNetwork(AbstractNetwork):
    pass


def regular_network(population, avg_connectivity=4):
    for player in population.values():
        player.neighbors = []

    radius = avg_connectivity / 2

    # Establish Network nodes for each member of the Population
    for member_counter in range(0, len(population)):
        # Each member will be assigned the surrounding neighbors according to the radius calculated
        # from the Average Number of Neighbors each member must have
        for distance in range(-int(radius), int(radius) + 1):
            # The cell itself is not a neighbor
            if distance == 0:
                continue

            # Obtain the Neighbor at the current distance
            neighbor_position = member_counter + distance
            if neighbor_position < 0:
                neighbor_position += len(population)
            elif neighbor_position >= len(population):
                neighbor_position -= len(population)

            # Add The Neighbor to the Current Member
            population[member_counter].neighbors.append(population[neighbor_position])


def scale_free_network(population, m=4, m0=2, undirected=False):
    """
    Generate Barrabasi-Albert scale-free network

    :param population: list of players in the population
    :param m:
    :param m0: initial number of nodes
    :param undirected:
    :return:
    """
    logger.info("Building scale-free network...")
    population_size = len(population)
    total_degree = 0

    # Create initial nodes
    for i in range(0, m0):
        player = population[i]
        for j in range(i+1, m0):
            new_neighbor = population[j]
            # Add the neighbor
            set_as_neighbor(player, new_neighbor)

            # Update network degree
            total_degree += 2

    # Connect new cells with previous cells
    for nodes_counter in range(m0, population_size):
        # Determine the number of edges to add
        edges2add = m0
        if nodes_counter < m0:
            edges2add = nodes_counter

        # Get population player/node
        player = population[nodes_counter]
        not_finished = True
        new_neighbor = None
        # Add as many random neighbors as Edges the player node has
        for edge_counter in range(0, edges2add):
            while not_finished:
                prob = random.uniform(0, 1)
                total_prob = len(population[0].neighbors) / total_degree
                new_neighbor = None
                for k in range(0, nodes_counter):
                    if prob < total_prob:
                        new_neighbor = population[k]
                        break
                    total_prob += len(population[k+1].neighbors) / total_degree
                not_finished = no_neighbor(new_neighbor, player)

            set_as_neighbor(player, new_neighbor)
            # Update Network Degree
            total_degree += 2

    logger.info("Finished building network.")


def barabasi_albert_graph(population, m=2, z=None, seed=None):
    """Return random graph using Barabási-Albert preferential attachment model.

    A graph of n nodes is grown by attaching new nodes each with m
    edges that are preferentially attached to existing nodes with high
    degree.

    Parameters
    ----------
    population: dict
                dictionary of player objects
    m : int
        Number of edges to attach from a new node to existing nodes
    z : average connectivity
    seed : int, optional
        Seed for random number generator (default=None).

    Returns
    -------
    G : Graph

    Notes
    -----
    The initialization is a graph with with m nodes and no edges.

    References
    ----------
    .. [1] A. L. Barabási and R. Albert "Emergence of scaling in
       random networks", Science 286, pp 509-512, 1999.
    """

    n = len(population)

    if z is not None:
        m = z//2

    if m < 1 or m >= n:
        raise ("Barabási-Albert network must have m>=1 and m<n, m=%d,n=%d" % (m, n))
    if seed is not None:
        random.seed(seed)

    # Target nodes for new edges
    targets = list(range(m))
    # List of existing nodes, with nodes repeated once for each adjacent edge
    repeated_nodes = []
    # Start adding the other n-m nodes. The first node is m.
    source = m
    while source < n:
        # Add edges to m nodes from the source.
        for i in targets:
            set_as_neighbor(population[i], population[source])
        # Add one node to the list for each new edge just created.
        repeated_nodes.extend(targets)
        # And the new node "source" has m edges to add to the list.
        repeated_nodes.extend([source]*m)
        # Now choose m unique nodes from the existing nodes
        # Pick uniformly from repeated_nodes (preferential attachement)
        targets = _random_subset(repeated_nodes, m)
        source += 1


def _random_subset(seq, m):
    """ Return m unique elements from seq.

    This differs from random.sample which can return repeated
    elements if seq holds repeated elements.
    """
    targets = set()
    while len(targets) < m:
        x = random.choice(seq)
        targets.add(x)
    return targets


def no_neighbor(neighbor, player):
    no = True
    if neighbor is not None:
        if neighbor.id != player.id:
            if not player.neighbors.__contains__(neighbor):
                no = False
    return no


def set_as_neighbor(player, new_neighbor):
    player.neighbors.append(new_neighbor)
    new_neighbor.neighbors.append(player)


def calculate_avg_connectivity(population):
    avg_connectivity = 0

    for index in range(len(population)):
        avg_connectivity = (avg_connectivity*index + len(population[index].neighbors)) / (index + 1)

    return avg_connectivity
