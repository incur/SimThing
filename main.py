import numpy as np


def main():
    pass


class TimeLine:
    def __init__(self):
        self.t_max = 20  # Simulationsdauer [s]
        self.dt = 0.001  # Zeitschrittweite [s]
        self.t = np.linspace(0, self.t_max, int(self.t_max / self.dt))


if __name__ == '__main__':
    main()
