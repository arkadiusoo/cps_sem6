import numpy as np
from assignment_3.correlation import (manual_correlation)
class RadarSimulator:
    def __init__(self, sampling_freq, signal_speed, signal_period, buffer_size, report_interval):
        """
        :param sampling_freq: częstotliwość próbkowania [Hz]
        :param signal_speed: prędkość propagacji sygnału [jedn. odległości / s]
        :param signal_period: okres sygnału sondującego [s]
        :param buffer_size: liczba próbek buforowanych
        :param report_interval: jak często wykonywać korelację [s]
        """
        self.Fs = sampling_freq
        self.dt = 1.0 / sampling_freq
        self.V = signal_speed
        self.T = signal_period
        self.N = buffer_size
        self.report_interval = report_interval

        self.time = np.linspace(0, self.N * self.dt, self.N, endpoint=False)

        # miejsce na wyniki
        self.distances = []

    def generate_probe_signal(self):
        # Sygnał złożony z dwóch sinusów
        f1, f2 = 1 / self.T, 2 / self.T
        return np.sin(2 * np.pi * f1 * self.time) + 0.5 * np.sin(2 * np.pi * f2 * self.time)

    def simulate_echo(self, distance, probe_signal):
        # Oblicz opóźnienie czasowe
        delay_time = 2 * distance / self.V
        delay_samples = int(delay_time * self.Fs)
        echo = np.zeros_like(probe_signal)
        if delay_samples < self.N:
            echo[delay_samples:] = probe_signal[:self.N - delay_samples]
        return echo

    def estimate_distance(self, probe_signal, echo_signal):
        """
        Oblicza korelację wzajemną i estymuje odległość na podstawie opóźnienia echa.
        """
        # Korelacja wzajemna (funkcja cross-correlation)
        correlation = manual_correlation(echo_signal, probe_signal, mode='linear')

        # Indeks środka (t = 0)
        center = len(correlation) // 2

        # Przeszukujemy tylko prawą połowę korelacji (dla t >= 0)
        right_half = correlation[center:]

        # Indeks maksimum korelacji w prawej połowie
        max_index = np.argmax(right_half)

        # Oblicz opóźnienie czasowe
        delay_time = max_index * self.dt

        # Oblicz odległość z S = V * t / 2
        distance = self.V * delay_time / 2

        # Zapisz do historii
        self.distances.append(distance)

        return distance, correlation