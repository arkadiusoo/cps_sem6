from PyQt6.QtWidgets import (
    QWidget, QLabel, QComboBox, QPushButton, QVBoxLayout,
    QHBoxLayout, QListWidget, QScrollArea, QMessageBox, QSpinBox
)

from assignment_1.plotting_utils import MatplotlibCanvas
from assignment_3.correlation import (manual_correlation, library_correlation, correlation_via_convolution)
from assignment_3.convolution import (manual_convolution, library_convolution)
from assignment_3.filter_design import (design_lowpass_fir_filter, design_highpass_fir_filter, apply_filter)
from assignment_3.radar_simulator import RadarSimulator

class Assignment4App(QWidget):
    def __init__(self, shared_signals=None):
        super().__init__()
        self.saved_signals = shared_signals if shared_signals else []
        self.results = []
        self.current_result = None
        self.plot_lines = {}  # Store references to plot lines
        self.plot_canvas = None  # Store reference to the current canvas
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Assignment 3 – Convolution, Filtering and Correlation")

        controls_layout = QVBoxLayout()

        self.combo_signal_selector = QComboBox()

        controls_layout.addWidget(QLabel("Wybierz pierwszy sygnał z Zadania 1:"))
        controls_layout.addWidget(self.combo_signal_selector)


        self.list_results = QListWidget()
        self.list_results.setFixedWidth(250)

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

    def update_signal_selector(self):
        self.combo_signal_selector.clear()
        for signal_info in self.saved_signals:
            self.combo_signal_selector.addItem(signal_info[0])

