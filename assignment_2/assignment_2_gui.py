from PyQt6.QtWidgets import (
    QWidget, QLabel, QComboBox, QSpinBox, QDoubleSpinBox, QPushButton,
    QVBoxLayout, QHBoxLayout, QSlider, QCheckBox
)
from PyQt6.QtCore import Qt


class SamplingQuantizationApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Assignment 2 – Sampling and Quantization")

        layout = QVBoxLayout()

        # Sampling settings
        label_sampling = QLabel("Sampling frequency (Częstotliwość próbkowania) [Hz]:")
        self.spin_sampling_freq = QDoubleSpinBox()
        self.spin_sampling_freq.setRange(1, 100000)
        self.spin_sampling_freq.setValue(1000)

        layout.addWidget(label_sampling)
        layout.addWidget(self.spin_sampling_freq)

        # Quantization settings
        label_quant_levels = QLabel("Quantization levels (Liczba poziomów kwantyzacji):")
        self.spin_quant_levels = QSpinBox()
        self.spin_quant_levels.setRange(2, 65536)
        self.spin_quant_levels.setValue(256)

        label_quant_method = QLabel("Quantization method (Metoda kwantyzacji):")
        self.combo_quant_method = QComboBox()
        self.combo_quant_method.addItems(["Truncation (Obcięcie)", "Rounding (Zaokrąglenie)"])

        layout.addWidget(label_quant_levels)
        layout.addWidget(self.spin_quant_levels)
        layout.addWidget(label_quant_method)
        layout.addWidget(self.combo_quant_method)

        # Reconstruction method
        label_reconstruction = QLabel("Reconstruction method (Metoda rekonstrukcji):")
        self.combo_reconstruction = QComboBox()
        self.combo_reconstruction.addItems([
            "Zero-order hold (ZOH)",
            "First-order hold (FOH)",
            "Sinc interpolation (Interpolacja sinc)"
        ])

        layout.addWidget(label_reconstruction)
        layout.addWidget(self.combo_reconstruction)

        # Aliasing examples
        label_aliasing = QLabel("Aliasing examples (Przykłady aliasingu):")
        self.combo_aliasing = QComboBox()
        self.combo_aliasing.addItems([
            "100 Hz, 1000 Hz",
            "440 Hz, 22050 Hz",
            "220 Hz, 44100 Hz"
        ])

        layout.addWidget(label_aliasing)
        layout.addWidget(self.combo_aliasing)

        # Additional options
        self.checkbox_show_metrics = QCheckBox("Show signal metrics (Pokaż parametry sygnału)")
        layout.addWidget(self.checkbox_show_metrics)

        # Buttons
        self.btn_generate = QPushButton("Generate and Analyze (Generuj i analizuj)")
        layout.addWidget(self.btn_generate)

        self.setLayout(layout)