from numpy import random


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
    population_size = len(population)
    total_degree = 0

    # Create initial nodes
    for i in range(0, m0 - 1):
        player = population[i]
        for j in range(i+1, i + m0):
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
