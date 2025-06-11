from PyQt6.QtWidgets import (
    QWidget, QLabel, QComboBox, QPushButton, QVBoxLayout,
    QHBoxLayout, QListWidget, QScrollArea, QMessageBox, QSpinBox, QCheckBox
)



# Import the transformation functions
from assignment_4.tranformation_methods import dft_from_definition, fft_from_definition, fft_walsh_hadamard_from_definition, fft_walsh_hadamard


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
            freq_domain, freq_axis = fft_from_definition(signal_data, duration)
        elif transform_type == "Transformacja Walsha-Hadamarda":
            freq_domain, freq_axis = fft_walsh_hadamard_from_definition(signal_data, duration)
        elif transform_type == "Szybka transformacja Walsha-Hadamarda":
            freq_domain, freq_axis = fft_walsh_hadamard(signal_data, duration)
        else:
            print("Invalid transformation type selected.")
            return

        # Now you have freq_domain and freq_axis for further processing (e.g., plotting)
        self.results = (freq_domain, freq_axis)
        print("Frequency domain:", freq_domain)
        print("Frequency axis:", freq_axis)
        self.plot_results()

    def plot_results(self):
        import matplotlib.pyplot as plt
        import numpy as np
        if self.results:
            freq_domain, freq_axis = self.results
            complex_display_mode = self.combo_complex_display.currentIndex()

            # Create a new figure for the plots
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))

            if complex_display_mode == 0:
                # Mode 3.1: Real part on the upper plot, Imaginary part on the lower plot
                ax1.plot(freq_axis, np.real(freq_domain), label="Re")
                ax1.set_title("Część rzeczywista (Re)")
                ax1.set_xlabel("Częstotliwość (Hz)")
                ax1.set_ylabel("Amplituda")

                ax2.plot(freq_axis, np.imag(freq_domain), label="Im", color="orange")
                ax2.set_title("Część urojona (Im)")
                ax2.set_xlabel("Częstotliwość (Hz)")
                ax2.set_ylabel("Amplituda")

            else:
                # Mode 3.2: Magnitude on the upper plot, Phase (argument) on the lower plot
                magnitude = np.abs(freq_domain)
                phase = np.angle(freq_domain)

                ax1.plot(freq_axis, magnitude, label="|Z|")
                ax1.set_title("Moduł (|Z|)")
                ax1.set_xlabel("Częstotliwość (Hz)")
                ax1.set_ylabel("Moduł")

                ax2.plot(freq_axis, phase, label="Arg(Z)", color="green")
                ax2.set_title("Faza (Arg(Z))")
                ax2.set_xlabel("Częstotliwość (Hz)")
                ax2.set_ylabel("Faza (radiany)")

            # Add grid to both plots
            ax1.grid(True)
            ax2.grid(True)

            # Adjust layout and show the plots
            plt.tight_layout()
            plt.show()