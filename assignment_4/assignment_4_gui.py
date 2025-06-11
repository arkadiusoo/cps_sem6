from PyQt6.QtWidgets import (
    QWidget, QLabel, QComboBox, QPushButton, QVBoxLayout,
    QHBoxLayout, QListWidget, QScrollArea, QMessageBox, QSpinBox
)

from assignment_1.plotting_utils import MatplotlibCanvas


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
        self.setWindowTitle("Assignment 4 – Transformations and Signal Visualization")

        controls_layout = QVBoxLayout()

        # Signal selector from previous task
        self.combo_signal_selector = QComboBox()
        controls_layout.addWidget(QLabel("Wybierz pierwszy sygnał z Zadania 1:"))
        controls_layout.addWidget(self.combo_signal_selector)

        # Row for Transformation Type
        self.label_transform_type = QLabel("Typ transformacji:")
        self.combo_transform_type = QComboBox()
        self.combo_transform_type.addItems([
            "Dyskretna transformata Fouriera (DFT)",
            "Szybka transformacja Fouriera (FFT) - decymacja w dziedzinie częstotliwości",
            "Transformacja Walsha-Hadamarda",
            "Szybka transformacja Walsha-Hadamarda"
        ])
        transform_row = QHBoxLayout()
        transform_row.addWidget(self.label_transform_type)
        transform_row.addWidget(self.combo_transform_type)
        controls_layout.addLayout(transform_row)

        # Row for Complex Signal Display Options
        self.label_complex_display = QLabel("Tryb wyświetlania sygnału zespolonego:")
        self.combo_complex_display = QComboBox()
        self.combo_complex_display.addItems([
            "Część rzeczywista / Część urojona",
            "Moduł / Faza"
        ])
        complex_row = QHBoxLayout()
        complex_row.addWidget(self.label_complex_display)
        complex_row.addWidget(self.combo_complex_display)
        controls_layout.addLayout(complex_row)

        self.btn_process = QPushButton("Wykonaj operację")
        self.btn_process.clicked.connect(self.perform_operation)
        controls_layout.addWidget(self.btn_process)


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

    # self.saved_signals[id][4][2] <- there is duration
    # self.saved_signals[id][0] <- there is name
    # self.saved_signals[id][1] <- there is signal list
    def perform_operation(self):
        print(self.saved_signals[0][4][2])