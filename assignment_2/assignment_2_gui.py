from PyQt6.QtWidgets import (
    QWidget, QLabel, QComboBox, QSpinBox, QDoubleSpinBox, QPushButton,
    QVBoxLayout, QHBoxLayout, QSlider, QCheckBox, QListWidget, QScrollArea
)

class SamplingQuantizationApp(QWidget):
    def __init__(self):
        super().__init__()
        self.saved_signals = []
        self.current_signal = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Assignment 2 – Sampling and Quantization")

        # === Controls Panel (Left side) ===
        controls_layout = QVBoxLayout()

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
