from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QListWidget
from PyQt6.QtCore import QTimer, QTime
import pyautogui
from .utils import show_error 

class AutoClickTimer(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Auto Click Timer")
        self.setGeometry(100, 100, 350, 520)
        self.setStyleSheet("background-color: #1e1e1e; color: white;")

        self.time_label = QLabel("00:00:00", self)
        self.time_label.setStyleSheet("font-size: 24px;")

        self.minute_input = QLineEdit(self)
        self.minute_input.setPlaceholderText("Menit")
        self.minute_input.setStyleSheet("background-color: #2e2e2e; color: white; padding: 5px;")

        self.second_input = QLineEdit(self)
        self.second_input.setPlaceholderText("Detik")
        self.second_input.setStyleSheet("background-color: #2e2e2e; color: white; padding: 5px;")

        self.add_button = QPushButton("Tambah", self)
        self.add_button.setStyleSheet("background-color: #4caf50; color: white; padding: 5px;")
        self.add_button.clicked.connect(self.add_time)

        self.list_widget = QListWidget(self)
        self.list_widget.setStyleSheet("background-color: #2e2e2e; color: white;")

        self.console_label = QLabel("Console", self)
        self.console_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 10px;")

        self.console_log = QListWidget(self)
        self.console_log.setStyleSheet("background-color: #121212; color: #00FF00; padding: 5px;")

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.minute_input)
        input_layout.addWidget(self.second_input)
        input_layout.addWidget(self.add_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.time_label)
        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.list_widget)
        main_layout.addSpacing(10)
        main_layout.addWidget(self.console_label)
        main_layout.addWidget(self.console_log)

        self.setLayout(main_layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

    def update_time(self):
        current_time = QTime.currentTime().toString("HH:mm:ss")
        self.time_label.setText(current_time)
        self.check_click(QTime.currentTime().minute(), QTime.currentTime().second())

    def add_time(self):
        try:
            minute_text = self.minute_input.text().strip()
            second = int(self.second_input.text().strip())

            if minute_text.upper() == "XX":
                minute_str = "XX"
            else:
                minute = int(minute_text)
                if 0 <= minute <= 9:
                    minute_str = f"X{minute}"
                else:
                    self.show_error("Masukkan angka 0-9 untuk menit atau 'XX'!")
                    return
                
            if 0 <= second <= 9:
                second_str = f"X{second}"
            else:
                self.show_error("Masukkan angka 0-9 untuk detik!")
                return

            self.list_widget.addItem(f"{minute_str}:{second_str}")
            self.minute_input.clear()
            self.second_input.clear()
        except ValueError:
            self.show_error("Masukkan angka yang valid!")

    
    def check_click(self, current_minute, current_second):
        for index in range(self.list_widget.count()):
            time_str = self.list_widget.item(index).text()
            try:
                minute_part, second_part = time_str.split(':')

                if minute_part == "XX":
                    stored_minute = None
                elif minute_part.startswith("X"):
                    stored_minute = int(minute_part[1:])
                else:
                    continue

                if second_part.startswith("X"):
                    stored_second = int(second_part[1:])
                else:
                    continue

                if (stored_minute is None or (current_minute % 10) == stored_minute) and current_second == stored_second:
                    current_time = QTime.currentTime().toString("HH:mm:ss")
                    log_message = f"[{current_time}] Click executed!"
                    
                    print(log_message)  # Debugging
                    self.console_log.addItem(log_message) 
                    self.console_log.scrollToBottom()  
                    pyautogui.click()
                    break
            except ValueError:
                continue 
