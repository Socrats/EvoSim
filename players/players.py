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
        self.neighbors = []
        self.action = 0
        self.prev_action = 0
        self.maxP = 0
        self.minP = 0
        self.inspected = 0

    def play_group_game(self, calculate_payoff, nu):
        game_players = [self, *self.neighbors]
        inspectors = []
        nc = 0
        ni = 0

        # Update nc and ni
        for player in [self, *self.neighbors]:
            player.inspected = 0
            if player.action == 0:
                nc += 1
            elif player.action == 2:
                ni += 1
                inspectors.append({'inspector': player, 'inspected': 0})
                game_players.remove(player)

        # If no cooperators, all players get 0 payoff (Tragedy of the commons)
        if nc == 0:
            for player in [self, *self.neighbors]:
                player.last_payoff = 0
                player.total_payoff += 0
                player.ngame += 1
            return

        # Calculate payoffs
        for player in game_players:
            player.update_payoff(calculate_payoff(player.action, nc, ni, len(self.neighbors)))

        if ni == 0:
            return

        # Inspection round

        inspectors_d = []
        # Find player
        for inspector in inspectors:
            inspected_player = game_players[random.randint(0, len(game_players))]
            if inspected_player.action:
                # Found a D
                inspector['inspected'] = inspected_player
                inspectors_d.append(inspector)
                inspected_player.inspected += 1
            else:
                inspector['inspector'].last_payoff = 0
                inspector['inspector'].total_payoff += 0
                inspector['inspector'].ngame += 1

        # Inspectors that found defectors
        for inspector in inspectors_d:
            payoff = (inspector['inspected'].last_payoff * float(nu)) / inspector['inspected'].inspected
            inspector['inspected'].set_inspected(-payoff)

            inspector['inspector'].last_payoff = payoff
            inspector['inspector'].total_payoff += payoff
            inspector['inspector'].ngame += 1

    def get_inspected_player(self, num_game_players):
        iid = random.randint(0, num_game_players)
        if self.neighbors[iid].action != 1:
            iid = -1
        return iid

    def set_inspected(self, payoff):
        self.last_payoff += payoff
        self.total_payoff += self.last_payoff

    def evolve(self, player):
        self.inspected = 0
        self.prev_action = self.action

        if self.total_payoff < player.total_payoff:
            prob = (player.total_payoff - self.total_payoff) / (player.maxP - self.minP)
            if random.uniform(0, 1) < prob:
                self.action = player.action

    def set_p_limit(self, local_max_p, local_min_p):
        self.maxP = 0
        self.minP = 0
        for player in [self, *self.neighbors]:
            self.maxP += local_max_p(len(player.neighbors))
            self.minP += local_min_p(len(player.neighbors))

    def init_params(self):
        super().init_params()
        self.inspected = 0

    def __str__(self):
        pass


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
