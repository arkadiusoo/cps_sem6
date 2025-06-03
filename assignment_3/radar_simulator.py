import numpy as np
from assignment_3.correlation import (manual_correlation)
class RadarSimulator:
    def __init__(self, sampling_freq, signal_speed, signal_period, buffer_size, report_interval, probe_signal):

        self.Fs = sampling_freq         # częstotliwość próbkowania
        self.dt = 1.0 / sampling_freq   # odstęp czasowy między próbkami
        self.V = signal_speed           # prędkość propagacji sygnału (np. dźwięku lub światła)
        self.T = signal_period          # okres fali sondującej - nieuzywane
        self.N = buffer_size            # długość bufora (ilość próbek sygnału)
        self.report_interval = report_interval
        self.probe_signal = probe_signal
        self.distances = []


    def simulate_echo(self, distance):
        # Oblicz opóźnienie czasowe
        delay_time = 2 * distance / self.V
        print("delay time w echo: {}".format(delay_time))
        delay_samples = int(delay_time * self.Fs)
        echo = np.zeros_like(self.probe_signal)
        if delay_samples < self.N:
            echo[delay_samples:] = self.probe_signal[:self.N - delay_samples]
        return echo

    def estimate_distance(self, echo_signal):

        # Oblicza korelację wzajemną i estymuje odległość na podstawie opóźnienia echa.

        # Korelacja wzajemna (funkcja cross-correlation)
        correlation = manual_correlation(echo_signal, self.probe_signal, mode='linear')
        print("korelcja:", correlation)
        # Indeks środka (t = 0)
        center = len(correlation) // 2

        # Przeszukujemy tylko prawą połowę korelacji (dla t >= 0)
        right_half = correlation[center:]

        # Indeks maksimum korelacji w prawej połowie
        max_index = np.argmax(right_half)
        print(right_half)

        # Oblicz opóźnienie czasowe
        delay_time = max_index * self.dt
        print("maks index: {}\nself.dt: {}".format(max_index, self.dt))
        print(delay_time)

        # Oblicz odległość z S = V * t / 2
        distance = self.V * delay_time / 2
        print("distance: {}".format(distance))

        # Zapisz do historii
        self.distances.append(distance)

        # return distance, correlation[center:]
        return distance, correlation