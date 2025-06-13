from PyQt6.QtWidgets import (
    QWidget, QLabel, QComboBox, QPushButton, QVBoxLayout,
    QHBoxLayout, QListWidget, QScrollArea, QMessageBox, QSpinBox, QCheckBox
)



# Import the transformation functions
from assignment_4.tranformation_methods import dft_from_definition, fft_from_definition, fft_walsh_hadamard_from_definition, fft_walsh_hadamard
from assignment_1.plotting_utils import MatplotlibCanvas

class Assignment4App(QWidget):
    def __init__(self, shared_signals=None):
        super().__init__()
        self.saved_signals = shared_signals if shared_signals else []
        self.results = []  # List of (label, (freq_domain, freq_axis, transform_type, signal_name, is_sample_signal))
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

        # Checkbox for "Przykładowy sygnał"
        self.checkbox_sample_signal = QCheckBox("Przykładowy sygnał")
        controls_layout.addWidget(self.checkbox_sample_signal)

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

    def update_signal_selector(self):
        self.combo_signal_selector.clear()
        for signal_info in self.saved_signals:
            self.combo_signal_selector.addItem(signal_info[0])

    # self.saved_signals[id][4][2] <- there is duration
    # self.saved_signals[id][0] <- there is name
    # self.saved_signals[id][1] <- there is signal list
    def perform_operation(self):
        # Retrieve the selected signal
        selected_signal_index = self.combo_signal_selector.currentIndex()
        if selected_signal_index < 0 or selected_signal_index >= len(self.saved_signals):
            print("No signal selected or invalid index.")
            return
        signal_info = self.saved_signals[selected_signal_index]
        signal_data = signal_info[1]  # The signal list
        duration = signal_info[4][2]

        # Retrieve the selected transformation type
        transform_type = self.combo_transform_type.currentText()

        # Get the state of the "Przykładowy sygnał" checkbox (third parameter)
        is_sample_signal = self.checkbox_sample_signal.isChecked()

        # Call the appropriate transformation function based on the selected type
        if transform_type == "Dyskretna transformata Fouriera (DFT)":
            freq_domain, freq_axis = dft_from_definition(signal_data, duration, is_sample_signal)
        elif transform_type == "Szybka transformacja Fouriera (FFT) - decymacja w dziedzinie częstotliwości":
            freq_domain, freq_axis = fft_from_definition(signal_data, duration, is_sample_signal)
        elif transform_type == "Transformacja Walsha-Hadamarda":
            freq_domain, freq_axis = fft_walsh_hadamard_from_definition(signal_data, duration)
        elif transform_type == "Szybka transformacja Walsha-Hadamarda":
            freq_domain, freq_axis = fft_walsh_hadamard(signal_data, duration)
        else:
            print("Invalid transformation type selected.")
            return

        # Build label for history
        label = f"[{len(self.results)+1}] {transform_type}: {signal_info[0]}"
        # Save result in history
        self.results.append((label, (freq_domain, freq_axis, transform_type, signal_info[0], is_sample_signal)))
        self.list_results.addItem(label)
        # Plot latest result
        self.plot_results()

    def plot_results(self, result=None):
        import numpy as np
        # Remove previous widgets (including previous plot) from scroll_layout
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        # Clear previous plot canvas reference
        self.plot_canvas = None

        # Determine which result to plot
        if result is not None:
            freq_domain, freq_axis, transform_type, signal_name, is_sample_signal = result
        elif self.results:
            # Use the latest result
            freq_domain, freq_axis, transform_type, signal_name, is_sample_signal = self.results[-1][1]
        else:
            return

        if transform_type == "Transformacja Walsha-Hadamarda" or transform_type == "Szybka transformacja Walsha-Hadamarda":
            self.label_complex_display.setVisible(False)
            self.combo_complex_display.setVisible(False)
            canvas = MatplotlibCanvas(self)
            freq_domain = [val[1] for val in freq_domain]
            freq_domain = np.array(freq_domain)
            canvas.ax.plot(freq_axis, freq_domain.real)
            canvas.ax.set_title(transform_type)
            canvas.ax.set_xlabel("Indeks")
            canvas.ax.set_ylabel("Amplituda")
            canvas.draw()
            self.scroll_layout.addWidget(canvas)
            self.plot_canvas = canvas
            return

        self.label_complex_display.setVisible(True)
        self.combo_complex_display.setVisible(True)
        complex_display_mode = self.combo_complex_display.currentIndex()

        # Create a MatplotlibCanvas and use two subplots
        canvas = MatplotlibCanvas(self)
        fig = canvas.figure
        fig.clear()
        ax1 = fig.add_subplot(2, 1, 1)
        ax2 = fig.add_subplot(2, 1, 2)

        x_data = np.arange(len(freq_domain))

        if complex_display_mode == 0:
            # Real/Imaginary
            ax1.plot(x_data, np.real(freq_domain), label="Re")
            ax1.set_title("Część rzeczywista (Re)")
            # ax1.set_xlabel("Częstotliwość (Hz)")
            ax1.set_ylabel("Amplituda")

            ax2.plot(x_data, np.imag(freq_domain), label="Im", color="orange")
            ax2.set_title("Część urojona (Im)")
            # ax2.set_xlabel("Częstotliwość (Hz)")
            ax2.set_ylabel("Amplituda")
        else:
            # Magnitude/Phase
            magnitude = np.abs(freq_domain)
            phase = np.angle(freq_domain)

            ax1.plot(x_data, magnitude, label="|Z|")
            ax1.set_title("Moduł (|Z|)")
            # ax1.set_xlabel("Częstotliwość (Hz)")
            ax1.set_ylabel("Moduł")

            ax2.plot(x_data, phase, label="Arg(Z)", color="green")
            ax2.set_title("Faza (Arg(Z))")
            # ax2.set_xlabel("Częstotliwość (Hz)")
            ax2.set_ylabel("Faza (radiany)")

        ax1.grid(True)
        ax2.grid(True)
        fig.tight_layout()
        canvas.draw()
        self.scroll_layout.addWidget(canvas)
        self.plot_canvas = canvas

        # Connect combo_complex_display to update the plot when toggled
        def on_display_mode_changed():
            # Redraw the currently selected result, or latest if none selected
            if self.list_results.currentRow() >= 0:
                idx = self.list_results.currentRow()
                _, res = self.results[idx]
                self.plot_results(res)
            else:
                self.plot_results()
        # Disconnect previous connections to avoid multiple triggers
        try:
            self.combo_complex_display.currentIndexChanged.disconnect()
        except Exception:
            pass
        self.combo_complex_display.currentIndexChanged.connect(on_display_mode_changed)

    def display_selected_result(self, item):
        idx = self.list_results.row(item)
        if idx < 0 or idx >= len(self.results):
            return
        label, result_tuple = self.results[idx]
        self.plot_results(result_tuple)