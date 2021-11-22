import matplotlib.pyplot as plt
import numpy as np
from devices.valve import ControlValve
from devices.heat_exchanger import WT
# from devices.pid import PID


def main():
    timeline = TimeLine(20)
    valve0 = ControlValve(timeline.dt)
    wt0 = WT(timeline)

    timeline.add_proc('ventilstellung', 0)
    timeline.add_proc('volumenstrom', 0)

    for now in range(1, len(timeline.t)):
        s, v = valve0.update()
        wt0.update(now, valve0.v_now)

        # Update Timeline
        timeline.write_proc('ventilstellung', now, s)
        timeline.write_proc('volumenstrom', now, v)

    plot_sim(timeline, valve0, wt0)


def plot_sim(timeline, valve0, wt0):
    fig = plt.figure(figsize=(10, 5))
    fig.set_tight_layout(True)

    ax1 = fig.add_subplot(2, 2, 1)
    ax1.set_xlabel('t [s]')
    ax1.set_ylabel('Ventil [%]')
    ax1.grid()
    ax1.plot(timeline.t, timeline.get_proc('ventilstellung'))

    ax2 = fig.add_subplot(2, 2, 2)
    ax2.set_xlabel('t [s]')
    ax2.set_ylabel('Volumenstrom [m³/h]')
    ax2.grid()
    ax2.plot(timeline.t, timeline.get_proc('volumenstrom'))

    ax3 = fig.add_subplot(2, 2, 3)
    ax3.set_xlabel('t [s]')
    ax3.set_ylabel('Produkt [°C]')
    ax3.grid()
    ax3.plot(timeline.t, wt0.r_warm)

    ax4 = fig.add_subplot(2, 2, 4)
    ax4.set_xlabel('t [s]')
    ax4.set_ylabel('Kühlwasser [°C]')
    ax4.grid()
    ax4.plot(timeline.t, wt0.r_kalt)

    plt.savefig('output/plot.png')


class TimeLine:
    def __init__(self, t_max):
        self.t_max = t_max  # Simulationsdauer [s]
        self.dt = 0.001  # Zeitschrittweite [s]
        self.t = np.linspace(0, self.t_max, int(self.t_max / self.dt))
        self.procs = {}

    def add_proc(self, name, startwert):
        self.procs[name] = np.zeros_like(self.t)
        self.write_proc(name, 0, startwert)

    def get_proc(self, name):
        return self.procs[name]

    def write_proc(self, name, now, value):
        self.procs[name][now] = value


if __name__ == '__main__':
    main()
