from PyQt6.QtWidgets import (
    QWidget, QLabel, QComboBox, QPushButton, QVBoxLayout,
    QHBoxLayout, QListWidget, QScrollArea, QMessageBox
)
from PyQt6.QtCore import Qt
from assignment_1.plotting_utils import MatplotlibCanvas

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
            "Korelacja – ręczna", "Korelacja – biblioteczna",
            "Filtracja – prostokątne okno",
            "Filtracja – Hamming", "Filtracja – Hanning", "Filtracja – Blackman"
        ])
        controls_layout.addWidget(QLabel("Wybierz operację:"))
        controls_layout.addWidget(self.combo_operation)

        self.combo_correlation_method = QComboBox()
        self.combo_correlation_method.addItems(["Liniowa", "Cyrkularna"])
        self.label_correlation_method = QLabel("Metoda korelacji:")
        controls_layout.addWidget(self.label_correlation_method)
        controls_layout.addWidget(self.combo_correlation_method)

        self.combo_filter_window = QComboBox()
        self.combo_filter_window.addItems(["Prostokątne", "Hamming", "Hanning", "Blackman"])
        self.label_filter_window = QLabel("Typ okna dla filtrowania:")
        controls_layout.addWidget(self.label_filter_window)
        controls_layout.addWidget(self.combo_filter_window)

        self.btn_apply_filter = QPushButton("Zastosuj filtr do sygnału")
        self.btn_apply_filter.clicked.connect(self.perform_operation)
        controls_layout.addWidget(self.btn_apply_filter)

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
        QMessageBox.information(self, "Info", "W tej wersji szkieletu operacja nie została jeszcze zaimplementowana.")

    def display_selected_result(self, item):
        index = self.list_results.row(item)
        label, t, y = self.results[index]

        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        canvas = MatplotlibCanvas(self)
        ax = canvas.ax
        ax.plot(t, y, label="Wynik operacji")
        ax.legend()
        ax.set_title(label)
        ax.set_xlabel("Czas [s]")
        ax.set_ylabel("Amplituda")
        ax.grid()
        canvas.draw()
        self.scroll_layout.addWidget(canvas)
        self.current_result = y

    def on_operation_changed(self):
        op = self.combo_operation.currentText()

        is_correlation = "Korelacja" in op
        is_filter = "Filtracja" in op
        is_two_signal = "Splot" in op or is_correlation

        self.combo_correlation_method.setVisible(is_correlation)
        self.label_correlation_method.setVisible(is_correlation)

        self.combo_filter_window.setVisible(is_filter)
        self.label_filter_window.setVisible(is_filter)

        self.combo_secondary_signal.setVisible(is_two_signal)
        self.label_secondary_signal.setVisible(is_two_signal)

        self.btn_apply_filter.setVisible(is_filter)
        self.btn_process.setVisible(not is_filter)