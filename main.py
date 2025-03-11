import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
                             QComboBox, QSpinBox, QFileDialog)


class SignalGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Generator Sygnałów")
        self.setGeometry(100, 100, 400, 300)

        # Wybór rodzaju sygnału
        self.label_signal = QLabel("Wybierz sygnał:")
        self.combo_signal = QComboBox()
        self.combo_signal.addItems(["Szum jednostajny", "Szum gaussowski", "Sygnał sinusoidalny",
                                    "Sygnał prostokątny", "Sygnał trójkątny"])

        # Parametry sygnału
        self.label_amp = QLabel("Amplituda:")
        self.spin_amp = QSpinBox()
        self.spin_amp.setRange(1, 100)

        self.label_duration = QLabel("Czas trwania:")
        self.spin_duration = QSpinBox()
        self.spin_duration.setRange(1, 10)

        # Przycisk generacji
        self.btn_generate = QPushButton("Generuj sygnał")
        self.btn_generate.clicked.connect(self.generate_signal)

        # Przycisk zapisu
        self.btn_save = QPushButton("Zapisz do pliku")
        self.btn_save.clicked.connect(self.save_signal)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label_signal)
        layout.addWidget(self.combo_signal)
        layout.addWidget(self.label_amp)
        layout.addWidget(self.spin_amp)
        layout.addWidget(self.label_duration)
        layout.addWidget(self.spin_duration)
        layout.addWidget(self.btn_generate)
        layout.addWidget(self.btn_save)

        self.setLayout(layout)

    def generate_signal(self):
        signal_type = self.combo_signal.currentText()
        amplitude = self.spin_amp.value()
        duration = self.spin_duration.value()
        time = np.linspace(0, duration, num=1000)

        if signal_type == "Szum jednostajny":
            signal = np.random.uniform(-amplitude, amplitude, size=len(time))
        elif signal_type == "Szum gaussowski":
            signal = np.random.normal(0, amplitude, size=len(time))
        elif signal_type == "Sygnał sinusoidalny":
            signal = amplitude * np.sin(2 * np.pi * time)
        elif signal_type == "Sygnał prostokątny":
            signal = amplitude * np.sign(np.sin(2 * np.pi * time))
        elif signal_type == "Sygnał trójkątny":
            signal = amplitude * np.abs(2 * (time % 1) - 1)
        else:
            signal = np.zeros(len(time))

        # Wizualizacja sygnału
        plt.figure()
        plt.plot(time, signal)
        plt.title(signal_type)
        plt.xlabel("Czas")
        plt.ylabel("Amplituda")
        plt.grid()
        plt.show()

        self.current_signal = signal

    def save_signal(self):
        if hasattr(self, 'current_signal'):
            file_name, _ = QFileDialog.getSaveFileName(self, "Zapisz plik", "", "Pliki binarne (*.bin)")
            if file_name:
                self.current_signal.tofile(file_name)
                print("Zapisano do pliku:", file_name)
        else:
            print("Najpierw wygeneruj sygnał!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SignalGeneratorApp()
    window.show()
    sys.exit(app.exec())
