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
        self.current_generation = 0

    def calculate_payoff(self, action):
        pass

    def init_game(self):
        pass

    def init_population(self, ncoop=0.5, ninsp=0.0):
        for player in self.population.values():
            prob = np.random.uniform(0, 1)
            action = 1
            if prob < ncoop:
                action = 0
            elif prob < (ncoop + ninsp):
                action = 2
            player.init_action(action)
            player.init_params()

    def run(self):
        avg_payoff = 0
        for self.current_generation in range(self.generations + self.threshold):
            # Count cooperators
            self.nc = 0
            for player in self.population.values():
                self.nc += (player.play(avg_payoff) - 1) % 2
            for player in self.population.values():
                player.update_payoff(self.calculate_payoff(player.action))
                avg_payoff += player.last_payoff

            avg_payoff /= len(self.population)
            if self.generations > self.threshold:
                self.coopLevel[self.current_generation-self.threshold] = self.nc / self.N
            logger.debug("[" + str(self.current_generation) + "] ncoop = " + str(self.nc))

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
        self.nc = 0
        # Get number of cooperators
        for player in self.population.values():
            player.set_m_payoffs(max_p=max_p, min_p=min_p)
            self.nc += 0 if player.action else 1

    def run(self):
        for self.current_generation in range(self.generations + self.threshold):
            # Calculate payoffs
            for player in self.population.values():
                player.update_payoff(self.calculate_payoff(player.action))
            # Evolve
            for player in self.population.values():
                # Call evolve and update number of cooperators
                dc, = player.evolve(self.population[np.random.randint(0, self.N)])
                self.nc += dc

            if self.generations > self.threshold:
                self.coopLevel[self.current_generation-self.threshold] = self.nc / self.N
            logger.debug("[" + str(self.current_generation) + "] ncoop = " + str(self.nc))


class PGGiGame(PGGGame):
    def __init__(self, population, threshold=0, generations=100, r=1.0, cost=1.0, nu=1.0):
        super().__init__(population, threshold=threshold, generations=generations, r=r, cost=cost)
        self.nu = nu
        self.ni = 0
        self.inspLevel = np.arange(0, generations, dtype=np.float64)

    def calculate_payoff(self, action):
        payoff = (self.nc*self.r*self.c)/(self.N - self.ni)
        if action:
            return payoff
        else:
            return payoff - self.c

    def get_inspected_player(self, pid):
        iid = np.random.randint(0, self.N)
        while iid == pid:
            iid = np.random.randint(0, self.N)
        if self.population[iid].action != 1:
            iid = -1
        return iid

    def inspect(self, inspector):
        pass

    def init_game(self):
        self.nc = self.N - 1
        self.ni = 0
        max_p = self.calculate_payoff(1)  # Max payoff
        self.nc = 1
        min_p = self.calculate_payoff(0)  # Min payoff
        self.nc = 0
        # Get number of cooperators
        for player in self.population.values():
            player.set_m_payoffs(max_p=max_p, min_p=min_p)
            self.nc += 0 if player.action else 1
            self.ni += 1 if (player.action == 2) else 0

    def run(self):
        for self.current_generation in range(self.generations + self.threshold):
            # Calculate payoffs
            for pid, player in self.population.items():
                if player.action != 2:
                    player.update_payoff(self.calculate_payoff(player.action))
                else:
                    iid = self.get_inspected_player(pid)
                    if iid == -1:
                        payoff = 0
                    else:
                        # Payoff for a D
                        payoff = float(self.calculate_payoff(1)) * float(self.nu)
                        self.population[iid].set_inspected(-payoff)
                    player.last_payoff = payoff
                    player.total_payoff += payoff
                    player.ngame += 1

            # Evolve
            self.nc = 0
            self.ni = 0
            for player in self.population.values():
                # Call evolve and update number of cooperators
                player.evolve(self.population[np.random.randint(0, self.N)])

                if player.action == 0:
                    self.nc += 1
                elif player.action == 2:
                    self.ni += 1

            logger.debug("[" + str(self.current_generation) + "] ncoop = " + str(self.nc) + " ninsp = " + str(self.ni))
            if self.generations > self.threshold:
                self.coopLevel[self.current_generation-self.threshold] = self.nc / self.N
                self.inspLevel[self.current_generation-self.threshold] = self.ni / self.N


class PGGiNetwork(PGGGame):
    def __init__(self, population, threshold=0, generations=100, r=1.0, cost=1.0, nu=1.0):
        super().__init__(population, threshold=threshold, generations=generations, r=r, cost=cost)
        self.nu = nu
        self.ni = 0
        self.inspLevel = np.arange(0, generations, dtype=np.float64)

    def calculate_payoff_game(self, action, nc, ni, k):
        payoff = (nc*self.r*self.c)/(k + 1 - ni)
        if action:
            return payoff
        else:
            return payoff - self.c

    def local_max_p(self, k):
        return (self.r*self.c*k)/(k+1)

    def local_min_p(self, k):
        return ((self.r/(k+1)) - 1)*self.c

    def init_game(self):
        pass

    def init_population(self, ncoop=0.5, ninsp=0.0):
        for player in self.population.values():
            prob = np.random.uniform(0, 1)
            action = 1
            if prob < ncoop:
                action = 0
            elif prob < (ncoop + ninsp):
                action = 2
            player.init_action(action)
            player.init_params()
            player.set_p_limit(self.local_max_p, self.local_min_p)

    def run(self):
        for self.current_generation in range(self.generations + self.threshold):
            # Calculate payoffs
            for player in self.population.values():
                player.play_group_game(self.calculate_payoff_game, self.nu)

            # Evolve
            self.nc = 0
            self.ni = 0
            for player in self.population.values():
                # Call evolve and update number of cooperators
                player.evolve(self.population[np.random.randint(0, self.N)])

                if player.action == 0:
                    self.nc += 1
                elif player.action == 2:
                    self.ni += 1

            logger.debug("[" + str(self.current_generation) + "] ncoop = " + str(self.nc) + " ninsp = " + str(self.ni))
            if self.generations > self.threshold:
                self.coopLevel[self.current_generation-self.threshold] = self.nc / self.N
                self.inspLevel[self.current_generation-self.threshold] = self.ni / self.N
