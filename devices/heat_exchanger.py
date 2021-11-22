import numpy
import numpy as np


def waermeaustausch(m_strom_warm, c_warm, m_strom_kalt, c_kalt,
                    in_warm, in_kalt, k, flaeche):
    """
    :param m_strom_warm: Massestrom Produktseite [Kg*s]
    :param c_warm: Wärmekapazität Produktseite [J/kgK]
    :param m_strom_kalt: Massestrom Kühlseite [Kg*s]
    :param c_kalt: Wärmekapazität Kühlseit [J/kgK]
    :param in_warm: Eintrittstemperatur Produktseite [K]
    :param in_kalt: Eintrittstemperatur Kühlseite
    :param k: Wärmekoeffizent [W/m²k]
    :param flaeche: Wärmeaustauschfläche [m²]
    :return: Austrittstemperatur Produktseite [K], Austrittstemperatur Kühlseite [K]
    """
    c_strom_warm = m_strom_warm * c_warm
    c_strom_kalt = m_strom_kalt * c_kalt + 0.0000001
    ntu_warm = (k * flaeche) / c_strom_warm
    ntu_kalt = (k * flaeche) / c_strom_kalt
    w1_w2 = c_strom_warm / c_strom_kalt
    w2_w1 = c_strom_kalt / c_strom_warm

    wirkung_warm = (1 - np.exp(-ntu_warm * 1 * (1 - w1_w2))) / (1 - w1_w2 * np.exp(-ntu_warm * (1 - w1_w2)))
    wirkung_kalt = (1 - np.exp(-ntu_kalt * 1 * (1 - w2_w1))) / (1 - w2_w1 * np.exp(-ntu_kalt * (1 - w2_w1)))

    if np.isnan(wirkung_warm) or np.isnan(wirkung_kalt):
        out_warm = in_warm
        out_kalt = in_kalt
    else:
        out_warm = in_warm - wirkung_warm * (in_warm - in_kalt) * 1
        out_kalt = in_kalt + (in_warm - in_kalt) * wirkung_kalt * 1

    return {'temp_out_warm': out_warm, 'temp_out_kalt': out_kalt}


def massestrom(volumenstrom, dichte):
    return (dichte * volumenstrom) / 3600


class WT:
    def __init__(self, timeline):
        self.flaeche = 5.37  # m²
        self.k = 1200  # W/m²k

        # Produktstrom
        self.waermekapazitaet_warm = 4186  # J/kgK
        self.eintritt_warm = 60  # °C
        self.massestrom_warm = (982.3 * 6.13) / 3600

        # Kühlmittelseite
        self.waermekapazitaet_kalt = 4179.8  # J/kgK
        self.eintritt_kalt = 20  # °C
        self.dichte_kalt = 997.2
        self.massestrom_kalt = massestrom(0, self.dichte_kalt)

        # Ausgang Fluide
        self.temp_now_produkt = self.eintritt_warm
        self.temp_now_kalt = self.eintritt_kalt

        # Simulation
        self.r_warm = np.zeros_like(timeline.t)
        self.r_warm[0] = self.temp_now_produkt
        self.r_kalt = np.zeros_like(timeline.t)
        self.r_kalt[0] = self.temp_now_kalt

    def update(self, now, volumenstrom):
        self.massestrom_kalt = massestrom(volumenstrom, self.dichte_kalt)

        t_out = waermeaustausch(self.massestrom_warm, self.waermekapazitaet_warm,
                                self.massestrom_kalt, self.waermekapazitaet_kalt,
                                self.eintritt_warm, self.eintritt_kalt, self.k, self.flaeche)

        self.r_warm[now] = t_out['temp_out_warm']
        self.r_kalt[now] = t_out['temp_out_kalt']

    def get_nowvalues_ma(self):
        low = self.eintritt_kalt
        high = self.eintritt_warm

        kalt_ma = np.interp(self.temp_now_kalt, (low, high), (4, 20))
        warm_ma = np.interp(self.temp_now_produkt, (low, high), (4, 20))

        return kalt_ma, warm_ma
