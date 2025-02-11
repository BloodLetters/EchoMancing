from PyQt6.QtWidgets import QMessageBox

def show_error(parent, message):
    error_box = QMessageBox(parent)
    error_box.setIcon(QMessageBox.Icon.Critical)
    error_box.setWindowTitle("Error")
    error_box.setText(message)
    error_box.setStyleSheet("background-color: #2e2e2e; color: white;")
    error_box.exec()
