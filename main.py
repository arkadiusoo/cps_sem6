import sys
import logging
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QComboBox, QSpinBox, QFileDialog
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import signal_generator
import file_manager

# Konfiguracja logowania błędów
logging.basicConfig(filename="app_errors.log", level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

# Klasa osadzonego wykresu Matplotlib w PyQt6
class MatplotlibCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)

    def plot(self, x, y, title="Wykres sygnału"):
        self.ax.clear()
        self.ax.plot(x, y, label=title)
        self.ax.set_title(title)
        self.ax.set_xlabel("Czas")
        self.ax.set_ylabel("Amplituda")
        self.ax.grid()
        self.ax.legend()
        self.draw()

class SignalGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.current_signal = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Generator Sygnałów")
        self.setGeometry(100, 100, 600, 400)  # Powiększamy okno

        # Wybór sygnału
        self.label_signal = QLabel("Wybierz sygnał:")
        self.combo_signal = QComboBox()
        self.combo_signal.addItems(["Szum jednostajny", "Szum gaussowski", "Sygnał sinusoidalny",
                                    "Sygnał prostokątny", "Sygnał trójkątny"])

        # Amplituda
        self.label_amp = QLabel("Amplituda:")
        self.spin_amp = QSpinBox()
        self.spin_amp.setRange(1, 100)

        # Czas trwania
        self.label_duration = QLabel("Czas trwania:")
        self.spin_duration = QSpinBox()
        self.spin_duration.setRange(1, 10)

        # Przycisk generacji
        self.btn_generate = QPushButton("Generuj sygnał")
        self.btn_generate.clicked.connect(self.generate_signal)

        # Przycisk zapisu
        self.btn_save = QPushButton("Zapisz do pliku")
        self.btn_save.clicked.connect(self.save_signal)

        # Widget Matplotlib do rysowania wykresów
        self.plot_canvas = MatplotlibCanvas(self)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label_signal)
        layout.addWidget(self.combo_signal)
        layout.addWidget(self.label_amp)
        layout.addWidget(self.spin_amp)
        layout.addWidget(self.label_duration)
        layout.addWidget(self.spin_duration)
        layout.addWidget(self.btn_generate)
        layout.addWidget(self.btn_save)
        layout.addWidget(self.plot_canvas)  # Dodajemy wykres do okna

        self.setLayout(layout)

    def generate_signal(self):
        try:
            signal_type = self.combo_signal.currentText()
            amplitude = self.spin_amp.value()
            duration = self.spin_duration.value()

            self.current_signal, time = signal_generator.generate_signal(signal_type, amplitude, duration)

            # Rysowanie wykresu w GUI
            self.plot_canvas.plot(time, self.current_signal, signal_type)

        except Exception as e:
            logging.error(f"Błąd podczas generowania sygnału: {e}")
            self.show_error_message("Błąd generowania sygnału", str(e))

    def save_signal(self):
        try:
            if self.current_signal is not None:
                file_name, _ = QFileDialog.getSaveFileName(self, "Zapisz plik", "", "Pliki binarne (*.bin)")
                if file_name:
                    file_manager.save_signal(file_name, self.current_signal)
            else:
                raise ValueError("Najpierw wygeneruj sygnał!")
        except Exception as e:
            logging.error(f"Błąd zapisu pliku: {e}")
            self.show_error_message("Błąd zapisu pliku", str(e))

    def show_error_message(self, title, message):
        from PyQt6.QtWidgets import QMessageBox
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SignalGeneratorApp()
    window.show()
    sys.exit(app.exec())
