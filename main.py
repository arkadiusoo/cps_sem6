import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QComboBox,
    QWidget, QVBoxLayout
)
from assignment_1.assignment_1_gui import SignalGeneratorApp


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Cyfrowe Przetwarzanie Sygnałów")
        self.setGeometry(100, 100, 1200, 800)

        # Dropdown (combo box) do wyboru zadania
        self.task_selector = QComboBox()
        self.task_selector.addItems(["Zadanie 1", "Zadanie 2"])
        self.task_selector.currentIndexChanged.connect(self.change_task)

        # Przestrzeń na widoki zadań
        self.stack = QStackedWidget()
        self.task1_widget = SignalGeneratorApp()
        self.task2_widget = QWidget()  # Placeholder – dodasz tu kolejne zadanie

        self.stack.addWidget(self.task1_widget)
        self.stack.addWidget(self.task2_widget)

        # Layout główny
        layout = QVBoxLayout()
        layout.addWidget(self.task_selector)
        layout.addWidget(self.stack)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Domyślnie pokazuj zadanie 1
        self.task_selector.setCurrentIndex(0)

    def change_task(self, index):
        self.stack.setCurrentIndex(index)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
