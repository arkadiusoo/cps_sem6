import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QTabWidget
)
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtCore import QRect

from assignment_1.assignment_1_gui import SignalGeneratorApp
from assignment_2.assignment_2_gui import SamplingQuantizationApp


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Cyfrowe Przetwarzanie Sygnałów")
        self.resize(1200, 800)

        # Center on second screen if available
        width, height = 1200, 800
        screens = QGuiApplication.screens()
        target_screen = screens[1] if len(screens) > 1 else screens[0]
        screen_geometry: QRect = target_screen.geometry()
        x = screen_geometry.x() + (screen_geometry.width() - width) // 2
        y = screen_geometry.y() + (screen_geometry.height() - height) // 2
        self.move(x, y)

        # Initialize widgets
        self.task1_widget = SignalGeneratorApp()
        self.task2_widget = SamplingQuantizationApp(self.task1_widget.saved_signals)

        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.addTab(self.task1_widget, "Zadanie 1")
        self.tabs.addTab(self.task2_widget, "Zadanie 2")

        self.tabs.currentChanged.connect(self.sync_signals)

        # Set layout
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def sync_signals(self, index):
        if index == 1:
            self.task2_widget.saved_signals = self.task1_widget.saved_signals
            self.task2_widget.combo_signal_selector.clear()
            for signal in self.task2_widget.saved_signals:
                self.task2_widget.combo_signal_selector.addItem(signal[0])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
