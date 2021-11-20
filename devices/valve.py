import numpy as np


class Valve:
    def __init__(self, timeline, dt):
        self.r0 = 0  # Startposition
        self.v0 = 10  # Geschwindigkeit [s]
        self.sp = 100  # Sollwert
        self.dt = dt * self.v0
        self.r = np.zeros_like(timeline)  # SimLine Ventilstellung
        self.r[0] = self.r0  # Startposition zuweisen
        self.v = np.zeros_like(timeline)  # SimLine Volumenstrom
        self.epsilon = self.v0 * dt  # Simulationstolleranz
        self.flowrate_table = []
        self.position_table = []
        self.min_flowrate = 0
        self.max_flowrate = 70
        self.v[0] = self.volumenstrom(self.r0)
        self.r_now = self.r0
        self.v_now = self.v[0]

    def update(self, now):
        prev = now-1

        # Ventil Charakteristik öffnen / schließen
        if abs(self.r[prev] - self.sp) < self.epsilon:
            self.r[now] = self.r[prev]
        elif self.r[prev] < self.sp:
            self.r[now] = self.r[prev] + self.dt
        elif self.r[prev] > self.sp:
            self.r[now] = self.r[prev] - self.dt

        self.v[now] = self.volumenstrom(self.r[now])
        self.r_now = self.r[now]
        self.v_now = self.v[now]

    def volumenstrom(self, position):
        ausgang = np.interp(position, self.flowrate_table, self.position_table)
        v = np.interp(ausgang, (0, 100), (self.min_flowrate, self.max_flowrate))
        return v

    def setpoint(self, sp):
        if sp <= 0:
            self.sp = 0
        elif sp >= 100:
            self.sp = 100
        else:
            self.sp = sp
