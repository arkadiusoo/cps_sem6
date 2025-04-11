import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QComboBox,
    QWidget, QVBoxLayout
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

        # Second screen if available, otherwise default
        width, height = 1200, 800
        screens = QGuiApplication.screens()
        target_screen = screens[1] if len(screens) > 1 else screens[0]
        screen_geometry: QRect = target_screen.geometry()

        x = screen_geometry.x() + (screen_geometry.width() - width) // 2
        y = screen_geometry.y() + (screen_geometry.height() - height) // 2
        self.move(x, y)

        self.task_selector = QComboBox()
        self.task_selector.addItems(["Zadanie 1", "Zadanie 2"])
        self.task_selector.currentIndexChanged.connect(self.change_task)

        self.stack = QStackedWidget()
        self.task1_widget = SignalGeneratorApp()
        self.task2_widget = SamplingQuantizationApp(self.task1_widget.saved_signals)

        self.stack.addWidget(self.task1_widget)
        self.stack.addWidget(self.task2_widget)

        layout = QVBoxLayout()
        layout.addWidget(self.task_selector)
        layout.addWidget(self.stack)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.task_selector.setCurrentIndex(0)

    def change_task(self, index):
        if index == 1:

            self.task2_widget.saved_signals = self.task1_widget.saved_signals


            self.task2_widget.combo_signal_selector.clear()
            for signal in self.task2_widget.saved_signals:
                self.task2_widget.combo_signal_selector.addItem(signal[0])

        self.stack.setCurrentIndex(index)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
