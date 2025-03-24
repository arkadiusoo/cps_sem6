import numpy as np
import logging
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox,
    QSpinBox, QFileDialog, QListWidget, QMessageBox
)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import signal_generator
import file_manager


class MatplotlibCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)

    def plot(self, x, y, title="Wykres sygnału"):
        self.ax.clear()
        self.ax.plot(x, y, label=title)
        self.ax.set_title(title)
        self.ax.set_xlabel("Czas")
        self.ax.set_ylabel("Amplituda")
        self.ax.grid()
        self.ax.legend()
        self.draw()


class SignalGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.current_signal = None
        self.signals_list = []  # Lista przechowywanych sygnałów
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Generator Sygnałów")
        self.setGeometry(100, 300, 1000, 600)

        # Wybór sygnału
        self.label_signal = QLabel("Wybierz sygnał:")
        self.combo_signal = QComboBox()
        self.combo_signal.addItems([
            "Szum jednostajny", "Szum gaussowski", "Sygnał sinusoidalny",
            "Sygnał prostokątny", "Sygnał trójkątny"
        ])

        # Amplituda
        self.label_amp = QLabel("Amplituda:")
        self.spin_amp = QSpinBox()
        self.spin_amp.setRange(1, 100)

        # Czas trwania
        self.label_duration = QLabel("Czas trwania:")
        self.spin_duration = QSpinBox()
        self.spin_duration.setRange(1, 10)

        # Przycisk generacji
        self.btn_generate = QPushButton("Generuj sygnał")
        self.btn_generate.clicked.connect(self.generate_signal)

        # Przycisk wczytywania
        self.btn_load = QPushButton("Wczytaj z pliku")
        self.btn_load.clicked.connect(self.load_signal)

        # Przycisk zapisu
        self.btn_save = QPushButton("Zapisz do pliku")
        self.btn_save.clicked.connect(self.save_signal)

        # Wykres
        self.plot_canvas = MatplotlibCanvas(self)

        # Lista wykresów
        self.list_signals = QListWidget()
        self.list_signals.setFixedWidth(250)
        self.list_signals.itemClicked.connect(self.display_selected_signal)

        # Layouty
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.label_signal)
        left_layout.addWidget(self.combo_signal)
        left_layout.addWidget(self.label_amp)
        left_layout.addWidget(self.spin_amp)
        left_layout.addWidget(self.label_duration)
        left_layout.addWidget(self.spin_duration)
        left_layout.addWidget(self.btn_generate)
        left_layout.addWidget(self.btn_load)
        left_layout.addWidget(self.btn_save)
        left_layout.addWidget(self.plot_canvas)

        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout)
        main_layout.addWidget(self.list_signals)

        self.setLayout(main_layout)

    def generate_signal(self):
        try:
            signal_type = self.combo_signal.currentText()
            amplitude = self.spin_amp.value()
            duration = self.spin_duration.value()

            self.current_signal, time = signal_generator.generate_signal(
                signal_type, amplitude, duration)

            self.plot_canvas.plot(time, self.current_signal, signal_type)

            signal_info = f"{signal_type} | A: {amplitude}, T: {duration}s"
            self.signals_list.append((time, self.current_signal, signal_info))
            self.list_signals.addItem(signal_info)

        except Exception as e:
            logging.error(f"Błąd podczas generowania sygnału: {e}")
            self.show_error_message("Błąd generowania sygnału", str(e))

    def save_signal(self):
        try:
            if self.current_signal is not None:
                file_name, _ = QFileDialog.getSaveFileName(
                    self, "Zapisz plik", "", "Pliki binarne (*.bin)")
                if file_name:
                    signal_type = self.combo_signal.currentText()
                    amplitude = self.spin_amp.value()
                    duration = self.spin_duration.value()
                    file_manager.save_signal(
                        file_name, self.current_signal, signal_type, amplitude, duration)
            else:
                raise ValueError("Najpierw wygeneruj sygnał!")
        except Exception as e:
            logging.error(f"Błąd zapisu pliku: {e}")
            self.show_error_message("Błąd zapisu pliku", str(e))

    def load_signal(self):
        try:
            file_name, _ = QFileDialog.getOpenFileName(
                self, "Otwórz plik", "", "Pliki binarne (*.bin)")
            if file_name:
                signal_type, amplitude, duration, signal = file_manager.load_signal(file_name)
                if signal is not None:
                    time = np.linspace(0, duration, len(signal))
                    self.plot_canvas.plot(time, signal, f"{signal_type} | A: {amplitude}, T: {duration}s")
                    signal_info = f"{signal_type} | A: {amplitude}, T: {duration}s"
                    self.signals_list.append((time, signal, signal_info))
                    self.list_signals.addItem(signal_info)
        except Exception as e:
            logging.error(f"Błąd odczytu pliku: {e}")
            self.show_error_message("Błąd odczytu pliku", str(e))

    def display_selected_signal(self, item):
        index = self.list_signals.row(item)
        time, signal, signal_info = self.signals_list[index]
        self.plot_canvas.plot(time, signal, signal_info)

    def show_error_message(self, title, message):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec()
