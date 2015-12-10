from uncertainpy import plotting

import pylab as plt
import numpy as np

class Spikes:
    def __init__(self):
        self.spikes = []
        self.nr_spikes = 0


    def spike_times(self, t, U):
        thresh = np.sqrt(U.var())

        print thresh
        # TODO Figure out exactly what this line does
        i, = np.where((U[:-1] < thresh) & (U[1:] > thresh))
        print i
        print t[i]
        print U[i]


    def detectSpikes(self, t, U):
        
        min_dist_from_peak = 2
        derivative_cutoff = 0.5

        self.spikes = []
        thresh = np.sqrt(U.var())

        start = 0
        start_flag = False
        dUdt = np.gradient(U)
        gt_derivative = np.where(dUdt >= -derivative_cutoff)[0]
        lt_derivative = np.where(dUdt <= derivative_cutoff)[0]

        for i in range(len(U)):
            if U[i] > thresh and start_flag is False:
                start = i
                start_flag = True
            elif U[i] < thresh and start_flag is True:
                start_flag = False

                t_spike = t[start:i + 1]
                U_spike = U[start:i + 1]

                spike_index = np.argmax(U_spike)
                global_index = spike_index + start
                t_max = t[global_index]
                U_max = U[global_index]

                spike_start = lt_derivative[np.where(lt_derivative < global_index - min_dist_from_peak)][-1]
                spike_end = gt_derivative[np.where(gt_derivative > global_index + min_dist_from_peak)][0]

                t_spike = t[spike_start:spike_end]
                U_spike = U[spike_start:spike_end]


                self.spikes.append(Spike(t_spike, U_spike, t_max, U_max, global_index))

        self.nr_spikes = len(self.spikes)


    def plot(self, save_name=None):
        color = 0
        u_max = []
        u_min = []
        t_max = []
        labels = []
        i = 1
        for spike in self.spikes:
            u_max.append(max(spike.U))
            u_min.append(min(spike.U))
            t_max.append(len(spike.t))
            plotting.prettyPlot(range(len(spike.t)), spike.U,
                                title="Spike",
                                xlabel="Time, ms",
                                ylabel="Voltage, mV",
                                color=color,
                                new_figure=False)
            labels.append("spike %d" % (i))
            color += 2
            i += 1


        plt.ylim([min(u_min), max(u_max)])
        plt.xlim([0, max(t_max)])
        plt.legend(labels)
        if save_name is None:
            plt.show()
        else:
            plt.savefig(save_name)


class Spike:
    def __init__(self, t_spike, U_spike, U_max, t_max, global_index):
        self.t = t_spike
        self.U = U_spike
        self.U_max = U_max
        self.t_max = t_max

        self.global_index = global_index


    def plot(self):
        plotting.prettyPlot(self.t, self.U, title="Spike", xlabel="Time, ms", ylabel="Voltage, mV", new_figure=True)
        plt.show()
