from PyQt6.QtWidgets import (
    QWidget, QLabel, QComboBox, QSpinBox, QDoubleSpinBox, QPushButton,
    QVBoxLayout, QHBoxLayout, QSlider, QCheckBox, QListWidget, QScrollArea, QMessageBox
)
from assignment_1.plotting_utils import MatplotlibCanvas
from assignment_2.quantization_functions import (
    sample_signal, quantize_signal, reconstruct_zoh,
    reconstruct_foh, reconstruct_sinc
)

import numpy as np

class SamplingQuantizationApp(QWidget):
    def __init__(self, shared_signals=None):
        super().__init__()
        self.saved_signals = shared_signals if shared_signals else []
        self.quantized_signals = []
        self.current_signal = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Assignment 2 – Sampling and Quantization")

        controls_layout = QVBoxLayout()
        self.combo_signal_selector = QComboBox()
        self.update_signal_selector()
        controls_layout.addWidget(QLabel("Wybierz sygnał z Zadania 1:"))
        controls_layout.addWidget(self.combo_signal_selector)

        self.spin_sampling_freq = QDoubleSpinBox()
        self.spin_sampling_freq.setRange(0.01, 100000)
        self.spin_sampling_freq.setValue(10)

        self.spin_quant_levels = QSpinBox()
        self.spin_quant_levels.setRange(1, 65536)
        self.spin_quant_levels.setValue(20)

        self.combo_quant_method = QComboBox()
        self.combo_quant_method.addItems(["Obcięcie", "Zaokrąglenie"])

        self.combo_reconstruction = QComboBox()
        self.combo_reconstruction.addItems([
            "Zero-order hold (ZOH)",
            "First-order hold (FOH)",
            "Interpolacja sinc"
        ])

        # self.combo_aliasing = QComboBox()
        # self.combo_aliasing.addItems([
        #     "100 Hz, 1000 Hz", "440 Hz, 22050 Hz", "220 Hz, 44100 Hz"
        # ])

        self.btn_generate = QPushButton("Generuj")
        self.btn_generate.clicked.connect(self.generate_and_plot)

        controls_layout.addWidget(QLabel("Częstotliwość próbkowania [Hz]:"))
        controls_layout.addWidget(self.spin_sampling_freq)
        controls_layout.addWidget(QLabel("Liczba poziomów kwantyzacji:"))
        controls_layout.addWidget(self.spin_quant_levels)
        controls_layout.addWidget(QLabel("Metoda kwantyzacji:"))
        controls_layout.addWidget(self.combo_quant_method)
        controls_layout.addWidget(QLabel("Metoda rekonstrukcji:"))
        controls_layout.addWidget(self.combo_reconstruction)
        # controls_layout.addWidget(QLabel("Przykłady aliasingu:"))
        # controls_layout.addWidget(self.combo_aliasing)
        controls_layout.addWidget(self.btn_generate)

        self.list_signals = QListWidget()
        self.list_signals.setFixedWidth(250)
        self.list_signals.itemClicked.connect(self.display_selected_signal)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_content.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_content)

        center_layout = QVBoxLayout()
        center_layout.addLayout(controls_layout)
        center_layout.addWidget(self.scroll_area)

        main_layout = QHBoxLayout()
        main_layout.addLayout(center_layout)
        main_layout.addWidget(self.list_signals)

        self.setLayout(main_layout)

    def update_signal_selector(self):
        self.combo_signal_selector.clear()
        for signal_info in self.saved_signals:
            self.combo_signal_selector.addItem(signal_info[0])

    def generate_and_plot(self):
        try:
            selected_index = self.combo_signal_selector.currentIndex()
            if selected_index < 0 or selected_index >= len(self.saved_signals):
                return

            label, original, _, _, _ = self.saved_signals[selected_index]
            y = [pt[0] for pt in original]
            t = [pt[1] for pt in original]

            fs = self.spin_sampling_freq.value()
            levels = self.spin_quant_levels.value()
            quant_method = self.combo_quant_method.currentText()
            reconstruction_method = self.combo_reconstruction.currentText()

            # Sample signal
            ts, ys = sample_signal(y, t, fs)

            # Quantize signal
            method = "truncate" if quant_method == "Obcięcie" else "round"
            ys_q = quantize_signal(ys, num_levels=levels, method=method)

            # Reconstruct signal
            if reconstruction_method.startswith("Zero"):
                reconstruction = reconstruct_zoh(ts, ys_q)
            elif reconstruction_method.startswith("First"):
                reconstruction = reconstruct_foh(ts, ys_q)
            else:
                reconstruction = reconstruct_sinc(ts, ys_q, t_range=(t[0], t[-1]))

            y_rec = [pt[0] for pt in reconstruction]
            t_rec = [pt[1] for pt in reconstruction]

            # Prepare name and store
            name = f"[{len(self.quantized_signals) + 1}]- {label} - fs={fs}Hz, Q={levels}"
            self.quantized_signals.append((name, t, y, ts, ys_q, t_rec, y_rec))
            self.list_signals.addItem(name)
            self.list_signals.setCurrentRow(self.list_signals.count() - 1)

            self.display_plot(name, t, y, ts, ys_q, t_rec, y_rec)

        except Exception as e:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Error Message")
            msg.setText(str(e))
            msg.exec()

    def display_selected_signal(self, item):
        index = self.list_signals.row(item)
        name, t, y, ts, ys_q, t_rec, y_rec = self.quantized_signals[index]
        self.display_plot(name, t, y, ts, ys_q, t_rec, y_rec)

    def display_plot(self, title, t, y, ts, ys_q, t_rec, y_rec):
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        canvas = MatplotlibCanvas(self)
        ax = canvas.ax
        ax.plot(t, y, label="Oryginalny")
        ax.plot(ts, ys_q, "ro", label="Próbki (kwantyzowane)")
        ax.plot(t_rec, y_rec, label="Rekonstrukcja")
        ax.set_title(title)
        ax.set_xlabel("Czas [s]")
        ax.set_ylabel("Amplituda")
        ax.grid()

        canvas.draw()

        self.scroll_layout.addWidget(canvas)
        self.current_signal = y
