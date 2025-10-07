from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFont
import traceback

class DebuggingPage(QWidget):
    def __init__(self, main_page=None, settings_page=None):
        super().__init__()
        self.main_page = main_page
        self.settings_page = settings_page
        self.init_ui()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_debug_info)
        self.timer.start(1000)

    def init_ui(self):
        layout = QVBoxLayout()
        title = QLabel('Debugging & Diagnostics')
        title.setFont(QFont('Arial', 20, QFont.Weight.Bold))
        layout.addWidget(title)

        self.debug_text = QTextEdit()
        self.debug_text.setReadOnly(True)
        self.debug_text.setFont(QFont('Consolas', 12))
        layout.addWidget(self.debug_text)

        refresh_btn = QPushButton('Refresh Now')
        refresh_btn.clicked.connect(self.update_debug_info)
        layout.addWidget(refresh_btn)

        self.setLayout(layout)
        self.update_debug_info()

    def update_debug_info(self):
        info = []
        try:
            if self.main_page:
                info.append('--- Main Page State ---')
                info.append(f'Selected Preset: {getattr(self.main_page, "selected_preset", None)}')
                info.append(f'Target Temperature: {getattr(self.main_page, "target_temperature", None)}')
                info.append(f'Remaining Time: {getattr(self.main_page, "remaining_time", None)}')
                info.append(f'Timer Running: {getattr(self.main_page, "timer_running", None)}')
                info.append(f'Temperature History: {getattr(self.main_page, "temperature_history", None)}')
                info.append(f'Humidity History: {getattr(self.main_page, "humidity_history", None)}')
            if self.settings_page:
                info.append('\n--- Settings Page State ---')
                info.append(f'Presets: {getattr(self.settings_page, "presets", None)}')
        except Exception as e:
            info.append('Error reading state:')
            info.append(traceback.format_exc())
        self.debug_text.setPlainText('\n'.join(str(i) for i in info))
