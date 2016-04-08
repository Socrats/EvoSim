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

    radius = avg_connectivity/2

    # Establish Network nodes for each member of the Population
    for member_counter in range(0, len(population)):
        # Each member will be assigned the surrounding neighbors according to the radius calculated
        # from the Average Number of Neighbors each member must have
        for distance in range(-int(radius), int(radius)+1):
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
