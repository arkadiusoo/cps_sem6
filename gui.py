import numpy as np
import logging
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox,
    QSpinBox, QFileDialog, QListWidget, QMessageBox, QDoubleSpinBox
)
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtCore import QRect
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
        # self.ax.legend()
        self.draw()


class SignalGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.current_signal = None
        self.signals_list = []  # Lista przechowywanych sygnałów
        self.init_ui()

    def init_ui(self):
        width, height = 1000, 600
        self.resize(width, height)
        # available screens
        screens = QGuiApplication.screens()

        # second screen if available otherwise first by default
        target_screen = screens[1] if len(screens) > 1 else screens[0]
        screen_geometry: QRect = target_screen.geometry()
        # center of the screen
        x = screen_geometry.x() + (screen_geometry.width() - width) // 2
        y = screen_geometry.y() + (screen_geometry.height() - height) // 2
        self.move(x, y)


        self.label_signal = QLabel("Wybierz sygnał:")
        self.combo_signal = QComboBox()
        self.combo_signal.addItems([
            "Szum jednostajny", "Szum gaussowski", "Sygnał sinusoidalny",
            "Sygnał prostokątny", "Sygnał trójkątny"
        ])

        self.label_signal_type = QLabel("Typ sygnału:")
        self.combo_signal_type = QComboBox()
        self.combo_signal_type.addItems(["Ciągły", "Dyskretny"])

        # A
        self.label_amp = QLabel("Amplituda (A):")
        self.spin_amp = QDoubleSpinBox()
        self.spin_amp.setRange(0.001, 100.0)
        self.spin_amp.setSingleStep(0.1)
        self.spin_amp.setDecimals(3)
        self.spin_amp.setValue(0.1)

        # d
        self.label_duration = QLabel("Czas trwania (d):")
        self.spin_duration = QDoubleSpinBox()
        self.spin_duration.setRange(0.001, 100.0)
        self.spin_duration.setSingleStep(0.1)
        self.spin_duration.setDecimals(3)
        self.spin_duration.setValue(1)

        # t1
        self.label_start_time = QLabel("Czas początkowy (t1):")
        self.spin_start_time = QDoubleSpinBox()
        self.spin_start_time.setRange(0.001, 100.0)
        self.spin_start_time.setSingleStep(0.1)
        self.spin_start_time.setDecimals(3)
        self.spin_start_time.setValue(0)

        # T
        self.label_period = QLabel("Okres podstawowy (T):")
        self.spin_period = QSpinBox()
        self.spin_period.setRange(1, 100)
        self.spin_period.setSingleStep(1)
        self.spin_period.setValue(5)

        # kw
        self.label_duty = QLabel("Współczynnik wypełnienia (k_w):")
        self.spin_duty = QDoubleSpinBox()
        self.spin_duty.setRange(0.01, 1.0)
        self.spin_duty.setSingleStep(0.05)
        self.spin_duty.setDecimals(2)
        self.spin_duty.setValue(0.5)

        # T_s
        self.label_sampling = QLabel("Okres próbkowania (T_s):")
        self.spin_sampling = QDoubleSpinBox()
        self.spin_sampling.setRange(0.001, 10.0)
        self.spin_sampling.setSingleStep(0.001)
        self.spin_sampling.setDecimals(4)
        self.spin_sampling.setValue(0.01)

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

        # layouts
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.label_signal)
        left_layout.addWidget(self.combo_signal)
        left_layout.addWidget(self.label_signal_type)
        left_layout.addWidget(self.combo_signal_type)
        left_layout.addWidget(self.label_amp)
        left_layout.addWidget(self.spin_amp)
        left_layout.addWidget(self.label_duration)
        left_layout.addWidget(self.spin_duration)
        left_layout.addWidget(self.label_start_time)
        left_layout.addWidget(self.spin_start_time)
        left_layout.addWidget(self.label_period)
        left_layout.addWidget(self.spin_period)
        left_layout.addWidget(self.label_duty)
        left_layout.addWidget(self.spin_duty)
        left_layout.addWidget(self.label_sampling)
        left_layout.addWidget(self.spin_sampling)
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
