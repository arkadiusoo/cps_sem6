from PyQt6.QtWidgets import (
    QWidget, QLabel, QComboBox, QPushButton, QVBoxLayout,
    QHBoxLayout, QListWidget, QScrollArea, QMessageBox, QSpinBox
)

from assignment_1.plotting_utils import MatplotlibCanvas
from assignment_3.correlation import (manual_correlation, library_correlation, correlation_via_convolution)
from assignment_3.convolution import (manual_convolution, library_convolution)
from assignment_3.filter_design import (design_lowpass_fir_filter, design_highpass_fir_filter, apply_filter)

class Assignment3App(QWidget):
    def __init__(self, shared_signals=None):
        super().__init__()
        self.saved_signals = shared_signals if shared_signals else []
        self.results = []
        self.current_result = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Assignment 3 – Convolution, Filtering and Correlation")

        controls_layout = QVBoxLayout()

        self.combo_signal_selector = QComboBox()

        controls_layout.addWidget(QLabel("Wybierz sygnał z Zadania 1:"))
        controls_layout.addWidget(self.combo_signal_selector)

        self.combo_secondary_signal = QComboBox()
        self.label_secondary_signal = QLabel("Wybierz drugi sygnał:")
        controls_layout.addWidget(self.label_secondary_signal)
        controls_layout.addWidget(self.combo_secondary_signal)

        self.combo_operation = QComboBox()
        self.combo_operation.addItems([
            "Splot – ręczny", "Splot – biblioteczny",
            "Korelacja – ręczna", "Korelacja przez splot - ręczna","Korelacja – biblioteczna",
            "Filtracja"
        ])
        controls_layout.addWidget(QLabel("Wybierz operację:"))
        controls_layout.addWidget(self.combo_operation)

        self.combo_correlation_method = QComboBox()
        self.combo_correlation_method.addItems(["Liniowa", "Cyrkularna"])
        self.label_correlation_method = QLabel("Metoda korelacji:")
        controls_layout.addWidget(self.label_correlation_method)
        controls_layout.addWidget(self.combo_correlation_method)

        self.combo_filter_type = QComboBox()
        self.combo_filter_type.addItems(["Dolnoprzepustowy", "Górnoprzepustowy"])
        self.label_filter_type = QLabel("Typ filtru:")
        controls_layout.addWidget(self.label_filter_type)
        controls_layout.addWidget(self.combo_filter_type)

        self.label_filter_length = QLabel("Liczba współczynników (M):")
        self.spin_filter_length = QSpinBox()
        self.spin_filter_length.setRange(11, 201)
        self.spin_filter_length.setSingleStep(2)
        self.spin_filter_length.setValue(51)
        controls_layout.addWidget(self.label_filter_length)
        controls_layout.addWidget(self.spin_filter_length)

        self.label_cutoff_freq = QLabel("Częstotliwość odcięcia [Hz]:")
        self.spin_cutoff_freq = QSpinBox()
        self.spin_cutoff_freq.setRange(10, 500)
        self.spin_cutoff_freq.setSingleStep(10)
        self.spin_cutoff_freq.setValue(200)
        controls_layout.addWidget(self.label_cutoff_freq)
        controls_layout.addWidget(self.spin_cutoff_freq)

        self.combo_filter_window = QComboBox()
        self.combo_filter_window.addItems(["Prostokątne", "Hamming", "Hanning", "Blackman"])
        self.label_filter_window = QLabel("Typ okna dla filtrowania:")
        controls_layout.addWidget(self.label_filter_window)
        controls_layout.addWidget(self.combo_filter_window)

        self.btn_process = QPushButton("Wykonaj operację")
        self.btn_process.clicked.connect(self.perform_operation)
        controls_layout.addWidget(self.btn_process)

        self.list_results = QListWidget()
        self.list_results.setFixedWidth(250)
        self.list_results.itemClicked.connect(self.display_selected_result)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_area.setWidget(self.scroll_content)

        center_layout = QVBoxLayout()
        center_layout.addLayout(controls_layout)
        center_layout.addWidget(self.scroll_area)

        main_layout = QHBoxLayout()
        main_layout.addLayout(center_layout)
        main_layout.addWidget(self.list_results)

        self.setLayout(main_layout)
        self.update_signal_selector()
        self.combo_operation.currentTextChanged.connect(self.on_operation_changed)
        self.on_operation_changed()

    def update_signal_selector(self):
        self.combo_signal_selector.clear()
        self.combo_secondary_signal.clear()
        for signal_info in self.saved_signals:
            self.combo_signal_selector.addItem(signal_info[0])
            self.combo_secondary_signal.addItem(signal_info[0])

    def perform_operation(self):
        import numpy as np

        op = self.combo_operation.currentText()
        idx1 = self.combo_signal_selector.currentIndex()
        idx2 = self.combo_secondary_signal.currentIndex()

        if idx1 < 0 or idx2 < 0 or idx1 >= len(self.saved_signals) or idx2 >= len(self.saved_signals):
            QMessageBox.warning(self, "Błąd", "Niepoprawny wybór sygnałów.")
            return

        name1, sig1, _, _, _ = self.saved_signals[idx1]
        name2, sig2, _, _, _ = self.saved_signals[idx2]

        short1 = " ".join(name1.split()[:3])
        short2 = " ".join(name2.split()[:3])

        x = [pt[0] for pt in sig1]
        y = [pt[0] for pt in sig2]
        t_x = [pt[1] for pt in sig1]

        result = []
        label = ""
        label_id = f"[{len(self.results) + 1}]"

        if "Splot" in op:
            if "ręczny" in op:
                result = manual_convolution(x, y)
                label = f"{label_id} Splot ręczny: {short1} * {short2}"
            else:
                result = library_convolution(x, y)
                label = f"{label_id} Splot biblioteczny: {short1} * {short2}"
            t_result = np.linspace(t_x[0], t_x[0] + len(result) / 1000, len(result))

        elif "Korelacja" in op:
            mode = self.combo_correlation_method.currentText().lower()  # 'liniowa' or 'cyrkularna'
            mode_eng = "linear" if mode == "liniowa" else "circular"

            if "ręczna" in op:
                result = manual_correlation(x, y, mode=mode_eng)
                label = f"{label_id} Korelacja {mode} ręczna: {short1} ⊛ {short2}"

            elif "przez splot" in op:
                result = correlation_via_convolution(x, y)
                label = f"{label_id} Korelacja poprzez splot ręczna: {short1} ⊛ {short2}"
            else:
                result = library_correlation(x, y, mode=mode_eng)
                label = f"{label_id} Korelacja {mode} biblioteczna: {short1} ⊛ {short2}"

            t_result = np.linspace(0, len(result) / 1000, len(result))


        elif "Filtracja" in op:


            window_name = self.combo_filter_window.currentText()
            window_type = window_name.lower()
            if window_type not in ["prostokątne", "hanning"]:
                QMessageBox.information(self, "Info", f"Typ okna {window_name} nieobsługiwany w tej wersji.")
                return

            # Normalizuj nazwę do wewnętrznej funkcji
            if window_type == "prostokątne":
                window_type = "rectangular"
            # Pobierz sygnał i czas
            signal_values = np.array([pt[0] for pt in sig1])
            time_values = np.array([pt[1] for pt in sig1])
            if len(time_values) < 2:
                QMessageBox.warning(self, "Błąd", "Brakuje danych czasowych do obliczenia częstotliwości próbkowania.")
                return

            dt = time_values[1] - time_values[0]
            Fs = 1 / dt
            fc = self.spin_cutoff_freq.value()
            M = self.spin_filter_length.value()
            if M % 2 == 0:
                QMessageBox.warning(self, "Błąd", "Liczba współczynników ma być nieparzysta.")
                return

            # Typ filtru (lowpass/highpass)
            filter_type = self.combo_filter_type.currentText().lower()
            if filter_type == "dolnoprzepustowy":
                filter_coeffs = design_lowpass_fir_filter(Fs, fc, M, window_type)
            elif filter_type == "górnoprzepustowy":
                filter_coeffs = design_highpass_fir_filter(Fs, fc, M, window_type)

            else:

                QMessageBox.warning(self, "Błąd", "Nieznany typ filtru.")

                return

            filtered_signal = apply_filter(signal_values, filter_coeffs)
            t_result = time_values[:len(filtered_signal)]
            label = f"{label_id} Filtracja – {window_name}, {filter_type}: {short1}"
            result = filtered_signal
            self.results.append((label, t_result, filtered_signal.tolist(), signal_values.tolist()))
            self.list_results.addItem(label)
            self.display_selected_result(self.list_results.item(self.list_results.count() - 1))
            return

        else:
            QMessageBox.information(self, "Info", "Wybrana operacja nie została jeszcze zaimplementowana.")
            return

        self.results.append((label, t_result, result))
        self.list_results.addItem(label)
        self.display_selected_result(self.list_results.item(self.list_results.count() - 1))

    def display_selected_result(self, item):
        index = self.list_results.row(item)
        data = self.results[index]

        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        canvas = MatplotlibCanvas(self)
        ax = canvas.ax

        if len(data) == 4:
            label, t, filtered, original = data
            # Make sure the arrays have the same length
            min_len = min(len(t), len(original), len(filtered))
            t = t[:min_len]
            original = original[:min_len]
            filtered = filtered[:min_len]

            ax.plot(t, original, label="Oryginalny sygnał")
            ax.plot(t, filtered, label="Sygnał przefiltrowany")
            ax.legend()
            ax.set_title(label)
            ax.set_xlabel("Czas [s]")
            ax.set_ylabel("Amplituda")
            ax.grid()
        else:
            label, t, y = data
            # Make sure the arrays have the same length
            min_len = min(len(t), len(y))
            t = t[:min_len]
            y = y[:min_len]

            ax.plot(t, y, label="Wynik operacji")
            ax.legend()
            ax.set_title(label)
            ax.set_xlabel("Czas [s]")
            ax.set_ylabel("Amplituda")
            ax.grid()

        canvas.draw()
        self.scroll_layout.addWidget(canvas)
        self.current_result = data[-1]

    def on_operation_changed(self):
        op = self.combo_operation.currentText()

        is_correlation = "Korelacja" in op
        is_correlation_by_convolution = "przez splot" in op
        is_filter = "Filtracja" in op
        is_two_signal = "Splot" in op or is_correlation

        self.combo_correlation_method.setVisible((is_correlation and not is_correlation_by_convolution) or (is_correlation_by_convolution and not is_correlation))
        self.label_correlation_method.setVisible((is_correlation and not is_correlation_by_convolution) or (is_correlation_by_convolution and not is_correlation))

        self.combo_filter_window.setVisible(is_filter)
        self.label_filter_window.setVisible(is_filter)

        self.combo_secondary_signal.setVisible(is_two_signal)
        self.label_secondary_signal.setVisible(is_two_signal)

        self.combo_filter_type.setVisible(is_filter)
        self.label_filter_type.setVisible(is_filter)

        self.btn_process.setVisible(True)
        self.spin_filter_length.setVisible(is_filter)
        self.label_filter_length.setVisible(is_filter)
        self.spin_cutoff_freq.setVisible(is_filter)
        self.label_cutoff_freq.setVisible(is_filter)