import numpy as np
import matplotlib.pyplot as plt
import logging
from time import time

logger = logging.getLogger(__name__)


class Simulation:
    """
    Simulation class:
    Generates a simulation object that defines all the characteristics of
    the simulation you want to run and holds all necessary elements to process and execute
    the simulation.

    name: Name of the simulation
    machine: local - run on a local machine
             remote - run on a remote machine
             hydra - run on hydra (an automatic configuration file for hydra will be generated)
             cluster -
    args:
    kwargs: you can pass a dictionary with all additional objects needed for the simulation
            - In case you choose remote, you should include here the IP/Port/User/Password of
            the remote machine
    """

    def __init__(self, name='default', machine='local', *args, **kwargs):
        self.name = name
        self.date_start = time()
        self.date_end = None
        self.time = None
        self.machine = machine
        self.args = args
        self.kwargs = kwargs
        self.__status = None
        for key, value in kwargs.items():  # styles is a regular dictionary
            setattr(self, key, value)
            logger.debug('key: %s, value: %s' % (key, value))

    def inject(self):
        pass

    def __next__(self):
        pass

    def __str__(self):
        string = '#Simulation ' + str(self.name) + ': Started at ' + str(self.date_start) + ' and to finish at ' + str(self.date_end) + '\n'
        string += '##Runing on ' + str(self.machine) + '\n'
        string += '##Status: ' + str(self.__status) + '\n'
        return string

    def run(self):
        x = np.arange(self.THRESHOLD, self.THRESHOLD + self.GENERATIONS)
        r_params = np.arange(self.r_min, self.r_max, self.r_step)
        coop_avg_run = np.empty([1, self.runs])
        insp_avg_run = np.empty([1, self.runs])
        coop_avg_real = np.empty([1, self.realizations])
        insp_avg_real = np.empty([1, self.realizations])
        coop_avg = np.arange(self.r_min, self.r_max, self.r_step)
        insp_avg = np.arange(self.r_min, self.r_max, self.r_step)

        if self.show_micro_simulations:
            plt.ion()  # Note this correction
            fig = plt.figure(1)
            ax = plt.axes(xlim=(-1, self.THRESHOLD + self.GENERATIONS), ylim=(-0.1, 1.2))

        for idx, r_param in enumerate(r_params):
            # Update r value
            logger.info("Starting simulation with r = %f", r_param)
            self.game.r = r_param
            r_start_time = time()
            for s in range(self.realizations):
                # Init graph
                for r in range(self.runs):
                    logger.debug("Realization %i, run %i", s, r)
                    start_time = time()
                    # Init game
                    self.game.init_game()
                    # Init population
                    self.game.init_population(ncoop=self.ncoop, ninsp=self.ninsp)
                    self.game.run()
                    interval = time() - start_time
                    logger.debug("elapsed time: %s seconds", interval)

                    # Update Avg.
                    coop_avg_run[0][r] = np.mean(self.game.coopLevel)
                    if self.game.__class__.__name__ == 'PGGiGame' or 'PGGiNetwork':
                        insp_avg_run[0][r] = np.mean(self.game.inspLevel)

                    if self.show_micro_simulations:
                        plt.cla()
                        # Save and Plot results
                        r_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)
                        r_text.set_text('r = %.3f' % r_param)
                        ax.plot(x, self.game.coopLevel, label='Fraction of cooperators', color='g', lw=2)
                        if self.game.__class__.__name__ == 'PGGiGame' or 'PGGiNetwork':
                            ax.plot(x, self.game.inspLevel, label='Fraction of inspectors', color='b', lw=2)
                        ax.set_xlabel("generations")
                        ax.set_ylabel("Fraction of players")
                        ax.set_ylim(-0.1, 1.2)
                        # plt.autoscale(True)
                        ax.legend()
                        plt.show()
                        plt.pause(0.0001)

                        # Init population
                        # game.init_population(ncoop=ncoop, ninsp=ninsp)

                # Update the Avg.
                coop_avg_real[0][s] = np.mean(coop_avg_run)
                if self.game.__class__.__name__ == 'PGGiGame' or 'PGGiNetwork':
                    insp_avg_real[0][s] = np.mean(insp_avg_run)

            coop_avg[idx] = np.mean(coop_avg_real)
            insp_avg[idx] = np.mean(insp_avg_real)
            r_interval = time() - r_start_time
            logger.info("Simulation finished: elapsed time: %s seconds", r_interval)

        if self.show_micro_simulations:
            plt.ioff()
        # Save and Plot results
        plt.figure(2)
        x_r = [r_param / (self.z + 1) for r_param in r_params]
        plt.plot(x_r, coop_avg, label='Fraction of cooperators', color='g')
        if self.game.__class__.__name__ == 'PGGiGame' or 'PGGiNetwork':
            plt.plot(x_r, insp_avg, label='Fraction of inspectors', color='b')
        plt.xlim(self.r_min / (self.z + 1), self.r_max / (self.z + 1))
        plt.ylim(-0.1, 1.2)
        plt.xlabel(r'$\eta = \frac{r}{z+1}$')
        plt.ylabel("Fraction of players")
        # plt.autoscale(True)
        plt.legend()
        plt.show()
