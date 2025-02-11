import sys
from PyQt6.QtWidgets import QApplication
from functions.ui import AutoClickTimer

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AutoClickTimer()
    window.show()
    sys.exit(app.exec())
