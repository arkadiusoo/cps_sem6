import numpy as np
import logging
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox,
    QSpinBox, QFileDialog, QListWidget, QMessageBox, QDoubleSpinBox,
    QSlider, QScrollArea
)
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtCore import QRect, Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import signal_generator
import file_manager


class MatplotlibCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = Figure(figsize=(5, 3))  # domyślny rozmiar figury
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)
        self.setMinimumHeight(300)  # <<< to ustawia minimum na wysokość

    def signal_plot(self, continuous_data, sampled_data, signal_type="Ciągły", title="Wykres sygnału"):
        self.ax.clear()

        # Unpack data: [time, value]
        t_cont, y_cont = continuous_data
        t_samp, y_samp = sampled_data

        # Draw original (continuous) function
        self.ax.plot(t_cont, y_cont, label="Funkcja oryginalna", color='blue')

        # Draw sampled points only if signal_type is 'Ciągły'
        if signal_type == "Ciągły":
            self.ax.plot(t_samp, y_samp, 'ro', label="Próbkowanie")  # czerwone kropki

        self.ax.set_title(title)
        self.ax.set_xlabel("Czas [s]")
        self.ax.set_ylabel("Amplituda")
        self.ax.grid()
        # self.ax.legend()
        self.draw()

    def plot_histogram(self, values, bins=10, title="Histogram amplitudy"):
        self.ax.clear()

        # Draw histogram
        self.ax.hist(values, bins=bins, color="darkorange", edgecolor="black")

        self.ax.set_title(title)
        self.ax.set_xlabel("Amplituda")
        self.ax.set_ylabel("Liczba wystąpień")
        self.ax.grid()
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
            "Sygnał sinusoidalny wyprostowany jednopołówkowo",
            "Sygnał sinusoidalny wyprostowany dwupołówkowo",
            "Sygnał prostokątny","Sygnał prostokątny symetryczny", "Sygnał trójkątny",
            "Skok jednostkowy", "Impuls jednostkowy", "Szum impulsowy"
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
        self.spin_amp.setValue(5)

        # d
        self.label_duration = QLabel("Czas trwania (d):")
        self.spin_duration = QDoubleSpinBox()
        self.spin_duration.setRange(0.001, 100.0)
        self.spin_duration.setSingleStep(0.1)
        self.spin_duration.setDecimals(3)
        self.spin_duration.setValue(3)

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
        self.label_duty = QLabel("Współ. wypełnienia (k_w):")
        self.spin_duty = QDoubleSpinBox()
        self.spin_duty.setRange(0.01, 1.0)
        self.spin_duty.setSingleStep(0.05)
        self.spin_duty.setDecimals(2)
        self.spin_duty.setValue(0.5)

        # T_s
        self.label_sampling = QLabel("Okres próbkowania (T_s):")
        self.spin_sampling = QDoubleSpinBox()
        self.spin_sampling.setRange(0.001, 100.0)
        self.spin_sampling.setSingleStep(0.001)
        self.spin_sampling.setDecimals(4)
        self.spin_sampling.setValue(0.01)

        # jump_time
        self.label_jump_time = QLabel("Okres próbkowania (T_s):")
        self.spin_jump_time = QDoubleSpinBox()
        self.spin_jump_time.setRange(0.001, 100.0)
        self.spin_jump_time.setSingleStep(0.001)
        self.spin_jump_time.setDecimals(4)
        self.spin_jump_time.setValue(0.01)

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
        # self.plot_canvas = MatplotlibCanvas(self)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_content.setLayout(self.scroll_layout)

        self.scroll_area.setWidget(self.scroll_content)

        # Lista wykresów
        self.list_signals = QListWidget()
        self.list_signals.setFixedWidth(250)
        self.list_signals.itemClicked.connect(self.display_selected_signal)

        self.label_bins = QLabel("Liczba przedziałów (bins):")
        self.slider_bins = QSlider(Qt.Orientation.Horizontal)
        self.slider_bins.setMinimum(5)
        self.slider_bins.setMaximum(20)
        self.slider_bins.setSingleStep(1)
        self.slider_bins.setTickInterval(1)
        self.slider_bins.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider_bins.setValue(10)  # Domyślna liczba binów

        self.label_bins_value = QLabel("10")  # Etykieta z aktualną wartością
        self.slider_bins.valueChanged.connect(self.on_bin_slider_changed)

        left_layout = QVBoxLayout()

        # Row 1
        row1 = QHBoxLayout()
        row1.addWidget(self.label_signal)
        row1.addWidget(self.combo_signal)
        row1.addWidget(self.label_signal_type)
        row1.addWidget(self.combo_signal_type)
        left_layout.addLayout(row1)

        # Row 2
        row2 = QHBoxLayout()
        row2.addWidget(self.label_amp)
        row2.addWidget(self.spin_amp)
        row2.addWidget(self.label_duration)
        row2.addWidget(self.spin_duration)
        left_layout.addLayout(row2)

        # Row 3
        row3 = QHBoxLayout()
        row3.addWidget(self.label_start_time)
        row3.addWidget(self.spin_start_time)
        row3.addWidget(self.label_period)
        row3.addWidget(self.spin_period)
        left_layout.addLayout(row3)

        # Row 4 – duty cycle only
        self.duty_row = QHBoxLayout()
        self.duty_row.addWidget(self.label_duty)
        self.duty_row.addWidget(self.spin_duty)
        left_layout.addLayout(self.duty_row)

        # Row 5 – sampling only
        self.sampling_row = QHBoxLayout()
        self.sampling_row.addWidget(self.label_sampling)
        self.sampling_row.addWidget(self.spin_sampling)
        left_layout.addLayout(self.sampling_row)

        # Row 6 - jumping only
        self.jump_time_row = QHBoxLayout()
        self.jump_time_row.addWidget(self.label_jump_time)
        self.jump_time_row.addWidget(self.spin_jump_time)
        left_layout.addLayout(self.jump_time_row)

        row_bins = QHBoxLayout()
        row_bins.addWidget(self.label_bins)
        row_bins.addWidget(self.slider_bins)
        row_bins.addWidget(self.label_bins_value)
        left_layout.addLayout(row_bins)

        # Buttons & plot
        left_layout.addWidget(self.btn_generate)
        left_layout.addWidget(self.btn_load)
        left_layout.addWidget(self.btn_save)
        # left_layout.addWidget(self.plot_canvas)
        left_layout.addWidget(self.scroll_area)

        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout)
        main_layout.addWidget(self.list_signals)

        # Update visibility connections
        self.combo_signal.currentTextChanged.connect(self.update_visibility_by_signal_type)
        self.combo_signal_type.currentTextChanged.connect(self.update_visibility_by_sampling_type)
        self.combo_signal.currentTextChanged.connect(self.update_visibility_by_jumping_type)

        self.setLayout(main_layout)
        self.update_visibility_by_signal_type()
        self.update_visibility_by_sampling_type()

    def generate_signal(self):
        try:

            signal_type = self.combo_signal.currentText()
            amplitude = self.spin_amp.value()
            duration = self.spin_duration.value()
            sampling_type = self.combo_signal_type.currentText()
            sampling_value = self.spin_sampling.value()
            duty_cycle = self.spin_duty.value()
            start_time = self.spin_start_time.value()
            period = self.spin_period.value()
            jump_time = self.spin_jump_time.value()

            signal_list = []
            sampling_list = []

            if signal_type == "Szum jednostajny":
                if sampling_type == "Dyskretny":
                    signal_list, sampling_list = signal_generator.uniform_dist_noise(amplitude, start_time, duration, sampling_value)
                else:
                    signal_generator.uniform_dist_noise(amplitude, start_time, duration)

            elif signal_type == "Szum gaussowski":
                if sampling_type == "Dyskretny":
                    signal_generator.gauss_noise(amplitude, start_time, duration, sampling_value)
                else:
                    signal_generator.gauss_noise(amplitude, start_time, duration)

            elif signal_type == "Sygnał sinusoidalny":
                if sampling_type == "Dyskretny":
                    pass
                else:
                    pass

            elif signal_type == "Sygnał sinusoidalny":
                if sampling_type == "Dyskretny":
                    signal_generator.sinus(amplitude, period, start_time, duration, sampling_value)
                else:
                    signal_generator.sinus(amplitude, period, start_time, duration)

            elif signal_type == "Sygnał sinusoidalny wyprostowany jednopołówkowo":
                if sampling_type == "Dyskretny":
                    signal_generator.sinus_abs(amplitude, period, start_time, duration, sampling_value)
                else:
                    signal_generator.sinus_abs(amplitude, period, start_time, duration)

            elif signal_type == "Sygnał sinusoidalny wyprostowany dwupołówkowo":
                if sampling_type == "Dyskretny":
                    signal_generator.sinus_one_half(amplitude, period, start_time, duration, sampling_value)
                else:
                    signal_generator.sinus_one_half(amplitude, period, start_time, duration)

            elif signal_type == "Sygnał prostokątny":
                if sampling_type == "Dyskretny":
                    signal_generator.square_classic(amplitude, period, start_time, duration, duty_cycle, sampling_value)
                else:
                    signal_generator.square_classic(amplitude, period, start_time, duration, duty_cycle)

            elif signal_type == "Sygnał prostokątny symetryczny":
                if sampling_type == "Dyskretny":
                    signal_generator.square_simetric(amplitude, period, start_time, duration, duty_cycle, sampling_value)
                else:
                    signal_generator.square_simetric(amplitude, period, start_time, duration, duty_cycle)

            elif signal_type == "Sygnał trójkątny":
                if sampling_type == "Dyskretny":
                    signal_generator.triangular(amplitude, period, start_time, duration, duty_cycle, sampling_value)
                else:
                    signal_generator.triangular(amplitude, period, start_time, duration, duty_cycle, sampling_value)

            elif signal_type == "Skok jednostkowy":
                if sampling_type == "Dyskretny":
                    signal_generator.jump_signal(amplitude, start_time, duration, jump_time, sampling_value)
                else:
                    signal_generator.jump_signal(amplitude, start_time, duration, jump_time, sampling_value)

            elif signal_type == "Impuls jednostkowy":
                if sampling_type == "Dyskretny":
                    pass
                else:
                    pass

            elif signal_type == "Szum impulsowy":
                if sampling_type == "Dyskretny":
                    pass
                else:
                    pass
            else:
                raise Exception("There is no such signal type! ({}).".format(signal_type))

            print(signal_list, sampling_list)
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
                    # self.plot_canvas.signal_plot(time, signal, f"{signal_type} | A: {amplitude}, T: {duration}s")
                    signal_info = f"{signal_type} | A: {amplitude}, T: {duration}s"
                    self.signals_list.append((time, signal, signal_info))
                    self.list_signals.addItem(signal_info)
        except Exception as e:
            logging.error(f"Błąd odczytu pliku: {e}")
            self.show_error_message("Błąd odczytu pliku", str(e))

    def display_selected_signal(self, item):
        index = self.list_signals.row(item)
        time, signal, signal_info = self.signals_list[index]
        # self.plot_canvas.signal_plot(time, signal, signal_info)

    def show_error_message(self, title, message):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec()

    def update_visibility_by_signal_type(self):
        signal_type = self.combo_signal.currentText()
        show_duty = signal_type in ["Sygnał prostokątny", "Sygnał trójkątny"]
        self.label_duty.setVisible(show_duty)
        self.spin_duty.setVisible(show_duty)

    def update_visibility_by_sampling_type(self):
        sampling_type = self.combo_signal_type.currentText()
        show_sampling = sampling_type == "Dyskretny"
        self.label_sampling.setVisible(show_sampling)
        self.spin_sampling.setVisible(show_sampling)

    def update_visibility_by_jumping_type(self):
        signal_type = self.combo_signal.currentText()
        show_jump = signal_type in ["Skok jednostkowy"]
        self.label_jump_time.setVisible(show_jump)
        self.spin_jump_time.setVisible(show_jump)

    def on_bin_slider_changed(self, value):
        self.label_bins_value.setText(str(value))
        if hasattr(self, "last_hist_canvas") and self.current_signal is not None:
            self.last_hist_canvas.plot_histogram(self.current_signal, bins=value)


