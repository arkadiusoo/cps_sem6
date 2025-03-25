import numpy as np
import logging
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox,
    QSpinBox, QFileDialog, QListWidget, QMessageBox, QDoubleSpinBox,
    QSlider, QScrollArea, QMenu, QInputDialog
)
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtCore import QRect, Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import signal_generator, file_manager, properties



class MatplotlibCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = Figure(figsize=(5, 4))
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)
        self.setMinimumHeight(300)
        self.saved_signals = []

    def signal_plot(self, continuous_data, sampled_data, signal_type="Ciągły", title="Wykres sygnału"):
        self.ax.clear()


        y_cont, t_cont = [], []
        y_samp, t_samp = [], []
        for el in continuous_data:
            y_cont.append(el[0])
            t_cont.append(el[1])
        for el in sampled_data:
            y_samp.append(el[0])
            t_samp.append(el[1])


        self.ax.plot(t_cont, y_cont, label="Funkcja oryginalna", color='blue')


        if signal_type == "Dyskretny":
            self.ax.plot(t_samp, y_samp, 'ro', label="Próbkowanie")

        self.ax.set_title(title)
        self.ax.set_xlabel("Czas [s]")
        self.ax.set_ylabel("Amplituda")
        self.ax.grid()
        # self.ax.legend()
        self.fig.tight_layout()
        self.draw()

    def plot_histogram(self, values, bins=10, title="Histogram amplitudy"):
        self.ax.clear()

        # Draw histogram
        self.ax.hist(values, bins=bins, color="darkorange", edgecolor="black")

        self.ax.set_title(title)
        self.ax.set_xlabel("Amplituda")
        self.ax.set_ylabel("Liczba wystąpień")
        self.ax.grid()
        self.fig.tight_layout()
        self.draw()


class SignalGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.current_signal = None
        self.saved_signals = []
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
        self.combo_signal.setCurrentText("Szum jednostajny")


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
        self.spin_sampling.setValue(30)
        self.label_sampling.setVisible(False)
        self.spin_sampling.setVisible(False)

        # jump_time
        self.label_jump_time = QLabel("Skok czasowy (jump_time):")
        self.spin_jump_time = QDoubleSpinBox()
        self.spin_jump_time.setRange(0.001, 100.0)
        self.spin_jump_time.setSingleStep(0.001)
        self.spin_jump_time.setDecimals(4)
        self.spin_jump_time.setValue(0.01)
        self.label_jump_time.setVisible(False)
        self.spin_jump_time.setVisible(False)

        # ns
        self.label_ns = QLabel("Numer próbki:")
        self.spin_ns  = QSpinBox()
        self.spin_ns.setRange(1, 100)
        self.spin_ns.setSingleStep(1)
        self.spin_ns.setValue(5)
        self.label_ns.setVisible(False)
        self.spin_ns.setVisible(False)

        # probability
        self.label_probability = QLabel("Prawdopodobieństwo:")
        self.spin_probability = QDoubleSpinBox()
        self.spin_probability.setRange(0.01, 1.0)
        self.spin_probability.setSingleStep(0.01)
        self.spin_probability.setDecimals(2)
        self.spin_probability.setValue(0.2)
        self.label_probability.setVisible(False)
        self.spin_probability.setVisible(False)

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
        self.list_signals.itemDoubleClicked.connect(self.show_signal_properties)
        self.list_signals.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.list_signals.customContextMenuRequested.connect(self.show_context_menu)

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

        # Row 7 - ns only
        self.ns_row = QHBoxLayout()
        self.ns_row.addWidget(self.label_ns)
        self.ns_row.addWidget(self.spin_ns)
        left_layout.addLayout(self.ns_row)
        # Row 8 - probability
        self.probability_row = QHBoxLayout()
        self.probability_row.addWidget(self.label_probability)
        self.probability_row.addWidget(self.spin_probability)
        left_layout.addLayout(self.probability_row)

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
        self.combo_signal.currentTextChanged.connect(self.update_visibility_by_sampling_type)
        self.combo_signal.currentTextChanged.connect(self.update_visibility_by_jumping_type)
        self.combo_signal.currentTextChanged.connect(self.update_visibility_by_ns_type)
        self.combo_signal.currentTextChanged.connect(self.update_visibility_by_probability_type)

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
            ns = self.spin_ns.value()
            probability = self.spin_probability.value()

            signal_list = []
            sampling_list = []

            if signal_type == "Szum jednostajny":
                if sampling_type == "Dyskretny":
                    signal_list, sampling_list = signal_generator.uniform_dist_noise(amplitude, start_time, duration, sampling_value)
                else:
                    signal_list, sampling_list = signal_generator.uniform_dist_noise(amplitude, start_time, duration)

            elif signal_type == "Szum gaussowski":
                if sampling_type == "Dyskretny":
                    signal_list, sampling_list = signal_generator.gauss_noise(amplitude, start_time, duration, sampling_value)
                else:
                    signal_list, sampling_list = signal_generator.gauss_noise(amplitude, start_time, duration)

            elif signal_type == "Sygnał sinusoidalny":
                if sampling_type == "Dyskretny":
                    signal_list, sampling_list = signal_generator.sinus(amplitude, period, start_time, duration, sampling_value)
                else:
                    signal_list, sampling_list = signal_generator.sinus(amplitude, period, start_time, duration)

            elif signal_type == "Sygnał sinusoidalny wyprostowany jednopołówkowo":
                if sampling_type == "Dyskretny":
                    signal_list, sampling_list = signal_generator.sinus_abs(amplitude, period, start_time, duration, sampling_value)
                else:
                    signal_list, sampling_list = signal_generator.sinus_abs(amplitude, period, start_time, duration)

            elif signal_type == "Sygnał sinusoidalny wyprostowany dwupołówkowo":
                if sampling_type == "Dyskretny":
                    signal_list, sampling_list = signal_generator.sinus_one_half(amplitude, period, start_time, duration, sampling_value)
                else:
                    signal_list, sampling_list = signal_generator.sinus_one_half(amplitude, period, start_time, duration)

            elif signal_type == "Sygnał prostokątny":
                if sampling_type == "Dyskretny":
                    signal_list, sampling_list = signal_generator.square_classic(amplitude, period, start_time, duration, duty_cycle, sampling_value)
                else:
                    signal_list, sampling_list = signal_generator.square_classic(amplitude, period, start_time, duration, duty_cycle)

            elif signal_type == "Sygnał prostokątny symetryczny":
                if sampling_type == "Dyskretny":
                    signal_list, sampling_list = signal_generator.square_simetric(amplitude, period, start_time, duration, duty_cycle, sampling_value)
                else:
                    signal_list, sampling_list = signal_generator.square_simetric(amplitude, period, start_time, duration, duty_cycle)

            elif signal_type == "Sygnał trójkątny":
                if sampling_type == "Dyskretny":
                    signal_list, sampling_list = signal_generator.triangular(amplitude, period, start_time, duration, duty_cycle, sampling_value)
                else:
                    signal_list, sampling_list = signal_generator.triangular(amplitude, period, start_time, duration, duty_cycle)

            elif signal_type == "Skok jednostkowy":
                if sampling_type == "Dyskretny":
                    signal_list, sampling_list = signal_generator.jump_signal(amplitude, start_time, duration, jump_time, sampling_value)
                else:
                    signal_list, sampling_list = signal_generator.jump_signal(amplitude, start_time, duration, jump_time)

            elif signal_type == "Impuls jednostkowy":
                if sampling_type == "Dyskretny":
                    signal_list, sampling_list = signal_generator.one_timer(amplitude, start_time, ns, duration, sampling_value)
                else:
                    signal_list, sampling_list = signal_generator.one_timer(amplitude, start_time, ns, duration, sampling_value)

            elif signal_type == "Szum impulsowy":
                if sampling_type == "Dyskretny":
                    signal_list, sampling_list = signal_generator.impulse_noise(amplitude, start_time, probability, duration, sampling_value)
                else:
                    signal_list, sampling_list = signal_generator.impulse_noise(amplitude, start_time, probability, duration, sampling_value)
            else:
                raise Exception("There is no such signal type! ({}).".format(signal_type))

            plot_title = "[{}] {} A: {} | T: {}s".format(len(self.saved_signals)+1,signal_type, amplitude, duration)
            print(plot_title)
            print("dlugosc sygnalu: {} | dlugosc probkowania: {}".format(len(signal_list), len(sampling_list)))
            # cleaning view
            for i in reversed(range(self.scroll_layout.count())):
                widget = self.scroll_layout.itemAt(i).widget()
                if widget:
                    widget.setParent(None)
            # signal plot
            canvas_func = MatplotlibCanvas(self)
            canvas_func.signal_plot(signal_list, sampling_list, signal_type=sampling_type, title=plot_title)
            self.scroll_layout.addWidget(canvas_func)

            # Histogram
            canvas_hist = MatplotlibCanvas(self)
            y = []
            for i in signal_list:
                y.append(i[0])
            canvas_hist.plot_histogram(y, bins=self.slider_bins.value(), title="Histogram amplitudy dla {}".format(plot_title))
            self.scroll_layout.addWidget(canvas_hist)

            # Dodaj do historii
            info = plot_title
            self.list_signals.addItem(info)
            self.saved_signals.append((info, signal_list, sampling_list, sampling_type, [signal_type,
                                                                                            amplitude,
                                                                                            duration,
                                                                                            sampling_type,
                                                                                            sampling_value,
                                                                                            duty_cycle,
                                                                                            start_time,
                                                                                            period,
                                                                                            jump_time,
                                                                                            ns,
                                                                                            probability]))

            # Zapisz ostatni sygnał do histogramu (dla slidera binów)
            self.current_signal = [i[0] for i in signal_list]
            self.last_hist_canvas = canvas_hist

            # Automatycznie zaznacz nowo dodany element
            new_index = self.list_signals.count() - 1
            self.list_signals.setCurrentRow(new_index)


        except Exception as e:
            logging.error(f"Błąd podczas generowania sygnału: {e}")
            self.show_error_message("Błąd generowania sygnału", str(e))

    def save_signal(self):
        try:
            if self.saved_signals:
                index = self.list_signals.currentRow()
                if index == -1:
                    raise ValueError("Nie wybrano sygnału do zapisania.")

                info, signal_list, sampling_list, sampling_type, parameters = self.saved_signals[index]

                file_name, _ = QFileDialog.getSaveFileName(
                    self, "Zapisz plik", "", "Pliki binarne (*.bin)")
                if file_name:
                    file_manager.save_signal(
                        file_name,
                        signal_list,
                        sampling_list,
                        sampling_type,
                        parameters
                    )
            else:
                raise ValueError("Brak sygnałów do zapisania.")
        except Exception as e:
            logging.error(f"Błąd zapisu pliku: {e}")
            self.show_error_message("Błąd zapisu pliku", str(e))

    def load_signal(self):
        try:
            file_name, _ = QFileDialog.getOpenFileName(
                self, "Otwórz plik", "", "Pliki binarne (*.bin)")
            if file_name:
                signal_list, sampling_list, sampling_type, parameters = file_manager.load_signal(file_name)

                signal_type = parameters[0]
                amplitude = parameters[1]
                duration = parameters[2]

                plot_title = f"[{len(self.saved_signals) + 1}] {signal_type} A: {amplitude} | T: {duration}s"

                # Rysowanie wykresu
                for i in reversed(range(self.scroll_layout.count())):
                    widget = self.scroll_layout.itemAt(i).widget()
                    if widget:
                        widget.setParent(None)

                canvas_func = MatplotlibCanvas(self)
                canvas_func.signal_plot(signal_list, sampling_list, signal_type=sampling_type, title=plot_title)
                self.scroll_layout.addWidget(canvas_func)

                canvas_hist = MatplotlibCanvas(self)
                y = [i[0] for i in signal_list]
                canvas_hist.plot_histogram(y, bins=self.slider_bins.value(),
                                           title=f"Histogram amplitudy dla {plot_title}")
                self.scroll_layout.addWidget(canvas_hist)

                # Dodanie do listy
                self.list_signals.addItem(plot_title)
                self.saved_signals.append((plot_title, signal_list, sampling_list, sampling_type, parameters))

                self.current_signal = y
                self.last_hist_canvas = canvas_hist

        except Exception as e:
            logging.error(f"Błąd odczytu pliku: {e}")
            self.show_error_message("Błąd odczytu pliku", str(e))

    def display_selected_signal(self, item):
        index = self.list_signals.row(item)
        info, signal_list, sampling_list, sampling_type, data = self.saved_signals[index]

        # Wyczyść poprzednie wykresy
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        # Stwórz i dodaj nowe płótno
        canvas_func = MatplotlibCanvas(self)
        canvas_func.signal_plot(signal_list, sampling_list, signal_type=sampling_type, title=info)
        self.scroll_layout.addWidget(canvas_func)

        canvas_hist = MatplotlibCanvas(self)
        y = [i[0] for i in signal_list]
        canvas_hist.plot_histogram(y, bins=self.slider_bins.value(), title="Histogram amplitudy dla {}".format(info))
        self.scroll_layout.addWidget(canvas_hist)

        self.current_signal = y
        self.last_hist_canvas = canvas_hist

        self.combo_signal.setCurrentText(data[0])
        self.spin_amp.setValue(data[1])
        self.spin_duration.setValue(data[2])
        self.combo_signal_type.setCurrentText(data[3])
        self.spin_sampling.setValue(data[4])
        self.spin_duty.setValue(data[5])
        self.spin_start_time.setValue(data[6])
        self.spin_period.setValue(int(data[7]))
        self.spin_jump_time.setValue(data[8])
        self.spin_ns.setValue(int(data[9]))
        self.spin_probability.setValue(data[10])

    def show_error_message(self, title, message):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec()

    def update_visibility_by_signal_type(self):
        signal_type = self.combo_signal.currentText()
        show_duty = signal_type in ["Sygnał prostokątny", "Sygnał trójkątny", "Sygnał prostokątny symetryczny"]
        self.label_duty.setVisible(show_duty)
        self.spin_duty.setVisible(show_duty)

    def update_visibility_by_sampling_type(self):
        sampling_type = self.combo_signal_type.currentText()
        signal_type = self.combo_signal.currentText()
        show_sampling = (sampling_type == "Dyskretny") or (signal_type in ["Impuls jednostkowy", "Szum impulsowy"])
        self.label_sampling.setVisible(show_sampling)
        self.spin_sampling.setVisible(show_sampling)

    def update_visibility_by_jumping_type(self):
        signal_type = self.combo_signal.currentText()
        show_jump = signal_type in ["Skok jednostkowy"]
        self.label_jump_time.setVisible(show_jump)
        self.spin_jump_time.setVisible(show_jump)

    def update_visibility_by_ns_type(self):
        signal_type = self.combo_signal.currentText()
        show_ns = signal_type in ["Impuls jednostkowy"]
        self.label_ns.setVisible(show_ns)
        self.spin_ns.setVisible(show_ns)

    def update_visibility_by_probability_type(self):
        signal_type = self.combo_signal.currentText()
        show_probability = signal_type in ["Szum impulsowy"]
        self.label_probability.setVisible(show_probability)
        self.spin_probability.setVisible(show_probability)

    def on_bin_slider_changed(self, value):
        self.label_bins_value.setText(str(value))
        if hasattr(self, "last_hist_canvas") and self.current_signal is not None:
            self.last_hist_canvas.plot_histogram(self.current_signal, bins=value)

    def show_signal_properties(self, item):
        index = self.list_signals.row(item)
        info, signal_list, sampling_list, sampling_type, data = self.saved_signals[index]

        # Używamy tylko sampling_list (bo to dane dyskretne)
        start = data[6]  # start_time
        end = start + data[2]  # start + duration

        try:
            mean_val = properties.mean_value_discreate(start, end, sampling_list)
            abs_mean_val = properties.absolute_mean_value_discreate(start, end, sampling_list)
            mean_power = properties.mean_power_discreate(start, end, sampling_list)
            variation = properties.variation_discreate(start, end, sampling_list)
            effective = properties.effective_value_discreate(start, end, sampling_list)

            summary = (
                f"<b>Informacje o sygnale {info}:</b><br><br>"
                f"<b>Właściwości sygnału:</b><br><br>"
                f"<b>Średnia:</b> {mean_val:.4f}<br>"
                f"<b>Średnia wartość bezwzględna:</b> {abs_mean_val:.4f}<br>"
                f"<b>Moc średnia:</b> {mean_power:.4f}<br>"
                f"<b>Wariancja:</b> {variation:.4f}<br>"
                f"<b>Wartość skuteczna:</b> {effective:.4f}"
            )

            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Właściwości sygnału")
            msg.setTextFormat(Qt.TextFormat.RichText)
            msg.setText(summary)
            msg.exec()
        except Exception as e:
            self.show_error_message("Błąd właściwości sygnału", str(e))

    from PyQt6.QtWidgets import QMenu

    def show_context_menu(self, position):
        index = self.list_signals.indexAt(position).row()
        if index < 0:
            return

        menu = QMenu(self)
        add_action = menu.addAction("Dodaj do innego sygnału")
        sub_action = menu.addAction("Odejmij od innego sygnału")
        mul_action = menu.addAction("Pomnóż przez inny sygnał")
        div_action = menu.addAction("Podziel przez inny sygnał")

        action = menu.exec(self.list_signals.mapToGlobal(position))

        if action:
            operation = None
            if action == add_action:
                operation = "add"
            elif action == sub_action:
                operation = "sub"
            elif action == mul_action:
                operation = "mul"
            elif action == div_action:
                operation = "div"

            if operation:
                self.perform_signal_operation(index, operation)


    def perform_signal_operation(self, base_index, operation):
        # Wyczyść poprzednie wykresy z layoutu
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        # Wybór drugiego sygnału
        items = [self.list_signals.item(i).text() for i in range(self.list_signals.count()) if i != base_index]
        if not items:
            self.show_error_message("Brak sygnałów", "Nie ma drugiego sygnału do wykonania operacji.")
            return

        item_text, ok = QInputDialog.getItem(self, "Wybierz drugi sygnał", "Drugi sygnał:", items, 0, False)
        if not ok or not item_text:
            return

        second_index = next(
            i for i in range(self.list_signals.count()) if self.list_signals.item(i).text() == item_text)

        # Pobierz dane
        _, signal1, _, _, _ = self.saved_signals[base_index]
        _, signal2, _, _, _ = self.saved_signals[second_index]

        # Zrównaj długości (minimum)
        min_len = min(len(signal1), len(signal2))
        sig1 = signal1[:min_len]
        sig2 = signal2[:min_len]

        result = []
        for (y1, t1), (y2, t2) in zip(sig1, sig2):
            if operation == "add":
                result.append([y1 + y2, t1])
            elif operation == "sub":
                result.append([y1 - y2, t1])
            elif operation == "mul":
                result.append([y1 * y2, t1])
            elif operation == "div":
                if y2 == 0:
                    result.append([0, t1])
                else:
                    result.append([y1 / y2, t1])

        # Zaktualizuj interfejs
        plot_title = f"Operacja ({operation}) [{len(self.saved_signals) + 1}]"
        self.list_signals.addItem(plot_title)
        self.saved_signals.append((plot_title, result, [], "Ciągły", ["Operacja", 0, 0, "Ciągły", 0, 0, 0, 0, 0, 0, 0]))

        canvas_func = MatplotlibCanvas(self)
        canvas_func.signal_plot(result, [], signal_type="Ciągły", title=plot_title)
        self.scroll_layout.addWidget(canvas_func)

        canvas_hist = MatplotlibCanvas(self)
        y = [pt[0] for pt in result]
        canvas_hist.plot_histogram(y, bins=self.slider_bins.value(),
                                   title="Histogram amplitudy dla {}".format(plot_title))
        self.scroll_layout.addWidget(canvas_hist)
