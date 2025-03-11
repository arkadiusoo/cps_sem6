import matplotlib.pyplot as plt
import numpy as np

def plot_signal(time, signal, title="Sygnał"):
    plt.figure(figsize=(8, 4))
    plt.plot(time, signal, label=title)
    plt.xlabel("Czas")
    plt.ylabel("Amplituda")
    plt.title(title)
    plt.grid()
    plt.legend()
    plt.show()

def plot_histogram(signal, bins=10):
    plt.figure(figsize=(6, 4))
    plt.hist(signal, bins=bins, edgecolor='black', alpha=0.7)
    plt.xlabel("Amplituda")
    plt.ylabel("Liczność")
    plt.title("Histogram sygnału")
    plt.grid()
    plt.show()
