import numpy
import numpy as np


class WT:
    def __init__(self, timeline, dt):
        self.flaeche = 5.37  # m²
        self.k = 1200  # W/m²k

        # Fluid Warm
        self.waermekapazitaet_warm = 4186  # J/kgK
        self.eintritt_warm = 60  # °C
        self.massestrom_warm = (982.3 * 6.13) / 3600

        # Fluid Kalt
        self.waermekapazitaet_kalt = 4179.8  # J/kgK
        self.eintritt_kalt = 20  # °C
        self.dichte_kalt = 997.2
        self.massestrom_kalt = self.massestrom(0)

        # Ausgang Fluide
        self.t_warm = self.eintritt_warm
        self.t_kalt = self.eintritt_kalt

        # Simulation
        self.r_warm = np.zeros_like(timeline)
        self.r_warm[0] = self.t_warm
        self.r_kalt = np.zeros_like(timeline)
        self.r_kalt[0] = self.t_kalt

    def massestrom(self, volumenstrom):
        return (self.dichte_kalt * volumenstrom) / 3600

    def update(self, now, volumenstrom):
        self.massestrom_kalt = self.massestrom(volumenstrom)

        # Hilfsgrößen
        waermekapazitaetstrom_warm = self.massestrom_warm * self.waermekapazitaet_warm  # J/K*s
        waermekapazitaetstrom_kalt = (self.massestrom_kalt * self.waermekapazitaet_kalt) + 0.0000001  # J/K*s
        ntu_warm = (self.k * self.flaeche) / waermekapazitaetstrom_warm
        ntu_kalt = (self.k * self.flaeche) / waermekapazitaetstrom_kalt
        w1_w2 = waermekapazitaetstrom_warm / waermekapazitaetstrom_kalt
        w2_w1 = waermekapazitaetstrom_kalt / waermekapazitaetstrom_warm

        wirkung_warm = (1 - np.exp(-ntu_warm * 1 * (1-w1_w2))) / (1 - w1_w2 * np.exp(-ntu_warm * (1-w1_w2)))
        wirkung_kalt = (1 - np.exp(-ntu_kalt * 1 * (1-w2_w1))) / (1 - w2_w1 * np.exp(-ntu_kalt * (1-w2_w1)))

        self.t_warm = self.eintritt_warm - wirkung_warm * (self.eintritt_warm - self.eintritt_kalt) * 1
        self.t_kalt = self.eintritt_kalt + (self.eintritt_warm - self.eintritt_kalt) * wirkung_kalt * 1

        self.r_warm[now] = self.t_warm
        self.r_kalt[now] = self.t_kalt
