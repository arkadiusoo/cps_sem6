from PyQt6.QtWidgets import (
    QWidget, QLabel, QComboBox, QSpinBox, QDoubleSpinBox, QPushButton,
    QVBoxLayout, QHBoxLayout, QSlider, QCheckBox, QListWidget, QScrollArea
)
from assignment_1.assignment_1_gui import MatplotlibCanvas
import numpy as np

class SamplingQuantizationApp(QWidget):
    def __init__(self, shared_signals=None):
        super().__init__()
        self.saved_signals = shared_signals if shared_signals else []
        self.current_signal = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Assignment 2 – Sampling and Quantization")

        # === Controls Panel (Left side) ===
        controls_layout = QVBoxLayout()

        self.combo_signal_selector = QComboBox()
        self.update_signal_selector()
        controls_layout.addWidget(QLabel("Wybierz sygnał z Zadania 1:"))
        controls_layout.addWidget(self.combo_signal_selector)

        label_sampling = QLabel("Częstotliwość próbkowania [Hz]:")
        self.spin_sampling_freq = QDoubleSpinBox()
        # self.spin_sampling_freq.setRange(1, 100000)
        self.spin_sampling_freq.setValue(1000)

        label_quant_levels = QLabel("Liczba poziomów kwantyzacji:")
        self.spin_quant_levels = QSpinBox()
        # self.spin_quant_levels.setRange(2, 65536)
        self.spin_quant_levels.setValue(256)

        label_quant_method = QLabel("Metoda kwantyzacji:")
        self.combo_quant_method = QComboBox()
        self.combo_quant_method.addItems(["Obcięcie", "Zaokrąglenie"])

        label_reconstruction = QLabel("Metoda rekonstrukcji:")
        self.combo_reconstruction = QComboBox()
        self.combo_reconstruction.addItems([
            "Zero-order hold (ZOH)",
            "First-order hold (FOH)",
            "Interpolacja sinc"
        ])

        label_aliasing = QLabel("Przykłady aliasingu:")
        self.combo_aliasing = QComboBox()
        self.combo_aliasing.addItems([
            "100 Hz, 1000 Hz",
            "440 Hz, 22050 Hz",
            "220 Hz, 44100 Hz"
        ])

        self.checkbox_show_metrics = QCheckBox("Pokaż parametry sygnału")
        self.btn_generate = QPushButton("Generuj")
        self.btn_generate.clicked.connect(self.generate_and_plot)


        controls_layout.addWidget(label_sampling)
        controls_layout.addWidget(self.spin_sampling_freq)
        controls_layout.addWidget(label_quant_levels)
        controls_layout.addWidget(self.spin_quant_levels)
        controls_layout.addWidget(label_quant_method)
        controls_layout.addWidget(self.combo_quant_method)
        controls_layout.addWidget(label_reconstruction)
        controls_layout.addWidget(self.combo_reconstruction)
        controls_layout.addWidget(label_aliasing)
        controls_layout.addWidget(self.combo_aliasing)
        controls_layout.addWidget(self.checkbox_show_metrics)
        controls_layout.addWidget(self.btn_generate)

        # === Right Side: Signal History ===
        self.list_signals = QListWidget()
        self.list_signals.setFixedWidth(250)

        # === Bottom: Plot Area ===
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_content.setLayout(self.scroll_layout)

        self.scroll_area.setWidget(self.scroll_content)

        # === Combine Layouts ===
        center_layout = QVBoxLayout()
        center_layout.addLayout(controls_layout)
        center_layout.addWidget(self.scroll_area)

        main_layout = QHBoxLayout()
        main_layout.addLayout(center_layout)
        main_layout.addWidget(self.list_signals)

        self.setLayout(main_layout)

    def set_saved_signals(self, signals):
        self.saved_signals = signals
        self.combo_signal_selector.clear()
        for signal in signals:
            self.combo_signal_selector.addItem(signal[0])

    def update_signal_selector(self):
        self.combo_signal_selector.clear()
        for signal_info in self.saved_signals:
            self.combo_signal_selector.addItem(signal_info[0])

    def generate_and_plot(self):

        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)


        selected_index = self.combo_signal_selector.currentIndex()
        if selected_index < 0 or selected_index >= len(self.saved_signals):
            return

        _, original, _, _, _ = self.saved_signals[selected_index]
        y = [pt[0] for pt in original]
        t = [pt[1] for pt in original]
        duration = t[-1] - t[0] if t else 1.0


        fs = self.spin_sampling_freq.value()
        ts = np.arange(t[0], t[0] + duration, 1 / fs)
        ys = np.interp(ts, t, y)


        levels = self.spin_quant_levels.value()
        quant_method = self.combo_quant_method.currentText()

        max_amp = max(abs(np.min(ys)), abs(np.max(ys)))
        step = 2 * max_amp / levels

        if quant_method == "Obcięcie":
            ys_q = (ys / step).astype(int) * step
        else:
            ys_q = np.round(ys / step) * step


        reconstruction_method = self.combo_reconstruction.currentText()
        t_rec = np.linspace(t[0], t[0] + duration, 1000)

        if reconstruction_method.startswith("Zero"):
            y_rec = np.zeros_like(t_rec)
            for i in range(len(ts) - 1):
                mask = (t_rec >= ts[i]) & (t_rec < ts[i + 1])
                y_rec[mask] = ys_q[i]
            y_rec[t_rec >= ts[-1]] = ys_q[-1]
        else:
            y_rec = np.interp(t_rec, ts, ys_q)


        canvas = MatplotlibCanvas(self)
        ax = canvas.ax
        ax.plot(t, y, label="Oryginalny")
        ax.plot(ts, ys_q, "ro", label="Próbki (kwantyzowane)")
        ax.plot(t_rec, y_rec, label="Rekonstrukcja")
        ax.set_title("Porównanie rekonstrukcji")
        ax.set_xlabel("Czas [s]")
        ax.set_ylabel("Amplituda")
        ax.grid()
        ax.legend()
        canvas.draw()

        self.scroll_layout.addWidget(canvas)
