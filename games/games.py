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
        self.coopLevel = np.arange(threshold, generations, dtype=np.float64)

    def calculate_payoff(self, action):
        pass

    def start_game(self):
        pass

    def run(self):
        avg_payoff = 0
        for i in range(self.generations):
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
            logger.debug("nc = " + str(self.nc) + " avg_payoff = " + str(avg_payoff))

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
    def __init__(self, threshold, generations, population, r, cost):
        super().__init__(threshold, generations, population)
        self.r = r
        self.c = cost

    def calculate_payoff(self, action):
        payoff = (self.nc*self.r*self.c)/self.N
        if action:
            return payoff
        else:
            return payoff - self.c
