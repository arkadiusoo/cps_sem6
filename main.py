import sys
import logging
from PyQt6.QtWidgets import QApplication
from gui import SignalGeneratorApp

# Konfiguracja logowania
logging.basicConfig(filename="app_errors.log", level=logging.ERROR,
                    format="%(asctime)s - %(levelname)s - %(message)s")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SignalGeneratorApp()
    window.show()
    sys.exit(app.exec())
