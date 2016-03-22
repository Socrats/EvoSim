import numpy as np
import matplotlib.pyplot as plt

from players.players_types import generate_players

N = 1000
HUMAN_PLAYER = True
PMATRIX = np.array([[0.8, 0.0],
                    [1.0, 0.2]])
GENERATIONS = 1000
cost = 1.0
r = 1.0
players = {}
xs = []
ys = []


def calculate_payoff(play, nc):
    if play:
        return (5 * nc + (N - nc - 1)) / (N - 1)
    else:
        return 3 * (nc - 1) / (N - 1)


def run():
    avg_payoff = 0
    for i in range(GENERATIONS):
        # Count cooperators
        nc = 0
        for player in players.values():
            nc += (player.play(avg_payoff) - 1) % 2
        for player in players.values():
            player.update_payoff(calculate_payoff(player.action, nc))
            avg_payoff += player.last_payoff
            # print(player)
        avg_payoff /= len(players)
        xs.append(i)
        ys.append(nc/N)
        print("nc = " + str(nc) + " avg_payoff = " + str(avg_payoff))

    plt.ioff()  # turn off interactive mode


if __name__ == "__main__":
    players = generate_players(N, [['TFTPlayer', 0.0], ['RandomPlayer', 0.0], ['ParlovPlayer', 1.0]])

    run()

    plt.plot(xs, ys)
    plt.autoscale(True)
    plt.show()
