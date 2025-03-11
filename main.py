import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QComboBox, QSpinBox, QFileDialog

import signal_generator
import plotter
import file_manager


class SignalGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.label_signal = None
        self.combo_signal = None
        self.spin_amp = None
        self.label_duration = None
        self.btn_generate = None
        self.btn_save = None
        self.spin_duration = None
        self.current_signal = None
        self.label_amp = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Generator Sygnałów")
        self.setGeometry(100, 100, 400, 300)

        self.label_signal = QLabel("Wybierz sygnał:")
        self.combo_signal = QComboBox()
        self.combo_signal.addItems(["Szum jednostajny", "Szum gaussowski", "Sygnał sinusoidalny",
                                    "Sygnał prostokątny", "Sygnał trójkątny"])

        self.label_amp = QLabel("Amplituda:")
        self.spin_amp = QSpinBox()
        self.spin_amp.setRange(1, 100)

        
        self.label_duration = QLabel("Czas trwania:")
        self.spin_duration = QSpinBox()
        self.spin_duration.setRange(1, 10)

        self.btn_generate = QPushButton("Generuj sygnał")
        self.btn_generate.clicked.connect(self.generate_signal)


        self.btn_save = QPushButton("Zapisz do pliku")
        self.btn_save.clicked.connect(self.save_signal)

        layout = QVBoxLayout()
        layout.addWidget(self.label_signal)
        layout.addWidget(self.combo_signal)
        layout.addWidget(self.label_amp)
        layout.addWidget(self.spin_amp)
        layout.addWidget(self.label_duration)
        layout.addWidget(self.spin_duration)
        layout.addWidget(self.btn_generate)
        layout.addWidget(self.btn_save)

        self.setLayout(layout)

    def generate_signal(self):
        signal_type = self.combo_signal.currentText()
        amplitude = self.spin_amp.value()
        duration = self.spin_duration.value()

        self.current_signal, time = signal_generator.generate_signal(signal_type, amplitude, duration)

        plotter.plot_signal(time, self.current_signal, signal_type)

    def save_signal(self):
        if hasattr(self, 'current_signal'):
            file_name, _ = QFileDialog.getSaveFileName(self, "Zapisz plik", "", "Pliki binarne (*.bin)")
            if file_name:
                file_manager.save_signal(file_name, self.current_signal)
        else:
            print("Najpierw wygeneruj sygnał!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SignalGeneratorApp()
    window.show()
    sys.exit(app.exec())
