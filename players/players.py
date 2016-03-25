import importlib
from numpy import random


class AbstractPlayer:
    def __init__(self, pid):
        self.id = pid
        self.ngame = 0
        self.prev_action = 0
        self.action = 0
        self.total_payoff = 0
        self.last_payoff = 0

    def play(self, avg_payoff):
        pass

    def update_payoff(self, payoff):
        self.last_payoff = payoff
        self.total_payoff += payoff
        self.ngame += 1

    def evolve(self, player):
        pass

    def init_action(self, action):
        self.action = action
        self.prev_action = action

    def __str__(self):
        return "Round " + str(self.ngame) + " " \
                                            "[" + str(self.id) + "] " + \
               ("D" if self.action else "C") + \
               " payoff= " + str(self.total_payoff)


class TFTPlayer(AbstractPlayer):
    def play(self, avg_payoff):
        self.prev_action = self.action
        if self.ngame > 0:
            self.action = 1 if (self.last_payoff - avg_payoff) < 0 else 0

        return self.action


class RandomPlayer(AbstractPlayer):
    def play(self, avg_payoff):
        self.prev_action = self.action
        self.action = 0 if random.uniform(0, 1) < 0.5 else 1

        return self.action


class ParlovPlayer(AbstractPlayer):
    def play(self, avg_payoff):
        self.prev_action = self.action
        if self.ngame > 0:
            self.action = (self.prev_action + 1) % 2 if (self.last_payoff - avg_payoff) < 0 else self.prev_action

        return self.action


class PureStrategyPlayer(AbstractPlayer):
    def __init__(self, pid):
        super().__init__(pid)
        self.M = 0
        self.action = 0
        self.prev_action = 0

    def play(self, avg_payoff):
        return self.action

    def evolve(self, player):
        self.prev_action = self.action
        if self.total_payoff < player.total_payoff:
            prob = (player.total_payoff - self.total_payoff) / self.M
            if random.uniform(0, 1) < prob:
                self.action = player.action
                # Return a 1 if changes to cooperate or else -1
                if self.action != self.prev_action:
                    return -1 if self.action else 1
        return 0

    def set_m(self, m):
        self.M = m


class HumanPlayer(AbstractPlayer):
    def play(self, avg_payoff):
        self.prev_action = self.action
        self.action = 0 if input('Choose C or D: ') == 'C' else 1

        return self.action


def players_factory(args):
    def factory():
        players = {}
        count = 0
        for name in args:
            if name == 'ncoop':
                continue
            for i in range(int(args[name])):
                player = getattr(importlib.import_module("players.players"), name)(count)
                player.init_action(0 if random.uniform(0, 1) < args['ncoop'] else 1)
                players[count] = player
                count += 1
        return players

    return factory


def generate_players(ratios, nplayers=10, ncoop=0.5):
    args = {'ncoop': ncoop}
    for ratio in ratios:
        args[ratio[0]] = ratio[1] * nplayers
    return players_factory(args)()
