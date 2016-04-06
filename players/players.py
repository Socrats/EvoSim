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

    def init_params(self):
        self.ngame = 0
        self.total_payoff = 0
        self.last_payoff = 0

    def __str__(self):
        return "Round " + str(self.ngame) + " " \
                                            "[" + str(self.id) + "] " + \
               {0: "C", 1: "D", 2: "I"}.get(self.action) + \
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
        self.action = 0
        self.prev_action = 0
        self.maxP = 0
        self.minP = 0
        self.payoff_inspected = 0
        self.inspected = False

    def init_params(self):
        super().init_params()
        self.payoff_inspected = 0
        self.inspected = False

    def play(self, avg_payoff):
        return self.action

    def evolve(self, player):
        if self.inspected:
            self.last_payoff -= self.payoff_inspected
        self.inspected = False
        self.prev_action = self.action

        if self.total_payoff < player.total_payoff:
            prob = (player.total_payoff - self.total_payoff) / (player.maxP - self.minP)
            if random.uniform(0, 1) < prob:
                self.action = player.action

    def set_m_payoffs(self, max_p=0, min_p=0):
        self.maxP = max_p
        self.minP = min_p

    def set_inspected(self, payoff):
        self.payoff_inspected = payoff
        self.total_payoff += payoff
        self.inspected = True


class PGGiPlayer(AbstractPlayer):
    def __init__(self, pid):
        super().__init__(pid)
        self.action = 0
        self.prev_action = 0
        self.maxP = 0
        self.minP = 0
        self.neighbors = {}

    def play(self, avg_payoff):
        return self.action

    def inspect(self):
        pass

    def evolve(self, player):
        self.prev_action = self.action
        if self.total_payoff < player.total_payoff:
            prob = (player.total_payoff - self.total_payoff) / (player.maxP - self.minP)
            if random.uniform(0, 1) < prob:
                self.action = player.action
                # Return a 1 if changes to cooperate or else -1
                if self.action != self.prev_action:
                    if self.prev_action == 0 and self.action > 0:
                        return -1
                    elif self.prev_action > 0 and self.action == 0:
                        return 1
        return 0

    def set_m_payoffs(self, max_p=0, min_p=0):
        self.maxP = max_p
        self.minP = min_p


class HumanPlayer(AbstractPlayer):
    def play(self, avg_payoff):
        self.prev_action = self.action
        self.action = 0 if input('Choose C or D: ') == 'C' else 1

        return self.action


# TODO: add init inspectors randomly
def players_factory(args):
    def factory():
        players = {}
        count = 0
        for name in args:
            if name == 'ncoop' or name == 'ninsp':
                continue
            for i in range(int(args[name])):
                player = getattr(importlib.import_module("players.players"), name)(count)
                prob = random.uniform(0, 1)
                if 'ninsp' in args.keys():
                    action = 1
                    if prob < args['ncoop']:
                        action = 0
                    elif prob < (args['ncoop'] + args['ninsp']):
                        action = 2
                    player.init_action(action)
                else:
                    player.init_action(0 if prob < args['ncoop'] else 1)
                players[count] = player
                count += 1
        return players

    return factory


def generate_players(ratios, nplayers=10, ncoop=0.5, ninsp=0.0):
    args = {'ncoop': ncoop, 'ninsp': ninsp}
    for ratio in ratios:
        args[ratio[0]] = ratio[1] * nplayers
    return players_factory(args)()
