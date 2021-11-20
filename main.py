import matplotlib.pyplot as plt
import numpy as np
from devices.valve import Valve
from devices.heat_exchanger import WT


def main():
    timeline = TimeLine()
    valve0 = Valve(timeline.t, timeline.dt)
    wt0 = WT(timeline.t, timeline.dt)

    for now in range(1, len(timeline.t)):
        prev = now-1

        valve0.update(now)
        wt0.update(now, valve0.v_now)

        plot_sim(timeline, valve0, wt0)


def plot_sim(timeline, valve0, wt0):
    fig = plt.figure(figsize=(10, 5))
    fig.set_tight_layout(True)

    ax1 = fig.add_subplot(2, 2, 1)
    ax1.set_xlabel('t [s]')
    ax1.set_ylabel('Ventil [%]')
    ax1.grid()
    ax1.plot(timeline.t, valve0.r)

    ax2 = fig.add_subplot(2, 2, 2)
    ax2.set_xlabel('t [s]')
    ax2.set_ylabel('Volumenstrom [m³/h]')
    ax2.grid()
    ax2.plot(timeline.t, valve0.v)

    ax3 = fig.add_subplot(2, 2, 3)
    ax3.set_xlabel('t [s]')
    ax3.set_ylabel('T_warm [°C]')
    ax3.grid()
    ax3.plot(timeline.t, wt0.r_warm)

    ax4 = fig.add_subplot(2, 2, 4)
    ax4.set_xlabel('t [s]')
    ax4.set_ylabel('T_kalt [°C]')
    ax4.grid()
    ax4.plot(timeline.t, wt0.r_kalt)

    plt.show()


class TimeLine:
    def __init__(self):
        self.t_max = 20  # Simulationsdauer [s]
        self.dt = 0.001  # Zeitschrittweite [s]
        self.t = np.linspace(0, self.t_max, int(self.t_max / self.dt))


if __name__ == '__main__':
    main()
