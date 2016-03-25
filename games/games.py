import numpy as np
import logging

logger = logging.getLogger(__name__)


class AbstractGame:
    def __init__(self, threshold, generations, population):
        self.threshold = threshold
        self.generations = generations
        self.population = population
        self.N = len(population)
        self.nc = 0
        self.coopLevel = np.arange(0, generations, dtype=np.float64)

    def calculate_payoff(self, action):
        pass

    def init_game(self):
        pass

    def run(self):
        avg_payoff = 0
        for i in range(self.generations + self.threshold):
            # Count cooperators
            self.nc = 0
            for player in self.population.values():
                self.nc += (player.play(avg_payoff) - 1) % 2
            for player in self.population.values():
                player.update_payoff(self.calculate_payoff(player.action))
                avg_payoff += player.last_payoff

            avg_payoff /= len(self.population)
            if self.generations > self.threshold:
                self.coopLevel[i-self.threshold] = self.nc / self.N
            logger.debug("[" + str(i) + "] ncoop = " + str(self.nc))

    def step(self):
        pass

    def stop(self):
        pass

    def reset(self):
        pass

    def pause(self):
        pass


class NIPDGame(AbstractGame):
    def calculate_payoff(self, action):
        if action:
            return (5 * self.nc + (self.N - self.nc - 1)) / (self.N - 1)
        else:
            return 3 * (self.nc - 1) / (self.N - 1)


class PGGGame(AbstractGame):
    def __init__(self, population, threshold=0, generations=100, r=1.0, cost=1.0):
        super().__init__(threshold, generations, population)
        self.r = r
        self.c = cost
        self.M = 0

    def calculate_payoff(self, action):
        payoff = (self.nc*self.r*self.c)/self.N
        if action:
            return payoff
        else:
            return payoff - self.c

    def init_game(self):
        self.nc = self.N - 1
        max_p = self.calculate_payoff(1)  # Max payoff
        self.nc = 1
        min_p = self.calculate_payoff(0)  # Min payoff
        self.M = max_p - min_p
        self.nc = 0
        # Get number of cooperators
        for player in self.population.values():
            player.set_m(self.M)
            self.nc += 0 if player.action else 1

    def run(self):
        for i in range(self.generations + self.threshold):
            # Calculate payoffs
            for player in self.population.values():
                player.update_payoff(self.calculate_payoff(player.action))
            # Evolve
            for player in self.population.values():
                # Call evolve and update number of cooperators
                self.nc += player.evolve(self.population[np.random.randint(0, self.N)])

            if self.generations > self.threshold:
                self.coopLevel[i-self.threshold] = self.nc / self.N
            logger.debug("[" + str(i) + "] ncoop = " + str(self.nc))
