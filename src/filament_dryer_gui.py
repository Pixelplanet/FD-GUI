import sys
import json
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QStatusBar, QMessageBox, QHBoxLayout)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from src.main_page import MainPage
from src.settings_page import SettingsPage
from src.debugging_page import DebuggingPage

class FilamentDryerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Filament Dryer Control System')
        # Set window to full screen for 7" touchscreen
        self.setWindowState(self.windowState() | Qt.WindowState.WindowFullScreen)

        # Create tab widget for navigation
        self.tabs = QTabWidget()
        self.tabs.setFont(QFont('Segoe UI', 18, QFont.Weight.Bold))
        self.tabs.setStyleSheet('''
            QTabBar::tab {
                height: 60px;
                font-size: 20pt;
                min-width: 180px;
                max-width: 180px;
                border-radius: 16px;
                background: #353941;
                color: #f0f0f0;
                margin: 4px;
                padding: 8px 24px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.15);
            }
            QTabBar::tab:selected {
                background: #0078d7;
                color: #fff;
                border: 2px solid #ff9800;
            }
            QTabBar { min-height: 60px; }
        ''')

        # Create pages
        self.main_page = MainPage()
        self.settings_page = SettingsPage()
        self.debugging_page = DebuggingPage(main_page=self.main_page, settings_page=self.settings_page)

        # Add tabs
        self.tabs.addTab(self.main_page, "Main")
        self.tabs.addTab(self.settings_page, "Settings")
        self.tabs.addTab(self.debugging_page, "Debug")

        # Status bar (move to top)
        self.status = QStatusBar()
        self.status.setStyleSheet('''
            QStatusBar {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #232629, stop:1 #353941);
                color: #ff9800;
                font-weight: bold;
                font-size: 20px;
                border-bottom: 2px solid #0078d7;
                min-height: 48px;
            }
        ''')


        self.status_label = QLabel("Temperature: 0°C | Humidity: --% | Status: Idle | Preset: None | Time Remaining: --:-- | Time: --:--:--")
        self.status_label.setFont(QFont('Segoe UI', 20, QFont.Weight.Bold))
        self.status_label.setMinimumHeight(48)
        self.status.addWidget(self.status_label)


        # Top bar widgets (current time and heater LED)
        self.top_bar = QWidget()
        top_bar_layout = QHBoxLayout()
        top_bar_layout.setContentsMargins(0, 0, 12, 0)
        top_bar_layout.addStretch()
        # Current time label
        self.time_label = QLabel()
        self.time_label.setFont(QFont('Segoe UI', 18, QFont.Weight.Bold))
        self.time_label.setStyleSheet('color: #ff9800;')
        top_bar_layout.addWidget(self.time_label)
        # Heater LED
        self.led_label = QLabel()
        self.led_label.setFixedSize(32, 32)
        self.led_label.setStyleSheet('border-radius: 16px; background: #353941; border: 2px solid #232629;')
        top_bar_layout.addWidget(self.led_label)
        self.top_bar.setLayout(top_bar_layout)

        # Add top bar to layout
        central_widget = QWidget()
        central_layout = QVBoxLayout()
        central_layout.setSpacing(0)
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.addWidget(self.top_bar)
        central_layout.addWidget(self.status)
        central_layout.addWidget(self.tabs)
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)

        # Timer for updating time and LED
        self.gui_timer = QTimer()
        self.gui_timer.timeout.connect(self.update_top_bar)
        self.gui_timer.start(1000)

        # Connect signals for navigation and preset updates
        self.main_page.switch_to_settings.connect(lambda: self.tabs.setCurrentWidget(self.settings_page))
        self.settings_page.switch_to_main.connect(lambda: self.tabs.setCurrentWidget(self.main_page))
        self.settings_page.presets_changed.connect(self.main_page.update_presets)

        # Initial status bar update
        self.update_status_bar()
        
    def update_status_bar(self):
        from datetime import datetime
        temp = self.main_page.temperature_label.text() if hasattr(self.main_page, 'temperature_label') else '--'
        preset_info = self.main_page.preset_info_label.text() if hasattr(self.main_page, 'preset_info_label') else '--'
        countdown = self.main_page.countdown_label.text() if hasattr(self.main_page, 'countdown_label') else '--:--'
        humidity = self.main_page.humidity_label.text() if hasattr(self.main_page, 'humidity_label') else '--'
        now = datetime.now().strftime('%H:%M:%S')
        self.status_label.setText(f"{temp} | {humidity} | {preset_info} | Time Remaining: {countdown} | Time: {now}")

    def update_top_bar(self):
        # Update LED color/brightness
        heater_on = getattr(self.main_page, 'heater_on', False)
        pwm_value = getattr(self.main_page, 'pwm_value', 0)
        # LED color: red if heater_on, else gray
        if heater_on:
            # Brightness based on PWM (0-255)
            brightness = int(80 + pwm_value * 0.7)  # 80-255
            self.led_label.setStyleSheet(f'border-radius: 16px; background: rgb({brightness},0,0); border: 2px solid #232629;')
        else:
            self.led_label.setStyleSheet('border-radius: 16px; background: #353941; border: 2px solid #232629;')
        # Also update the status bar to refresh the time
        self.update_status_bar()

def main():
    app = QApplication(sys.argv)
    # Modern dark theme using Qt stylesheets
    dark_stylesheet = """
    QWidget { background-color: #232629; color: #f0f0f0; font-family: 'Segoe UI', Arial, sans-serif; }
    QTabBar::tab { background: #353941; color: #f0f0f0; border-radius: 16px; margin: 4px; padding: 8px 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.15); }
    QTabBar::tab:selected { background: #0078d7; color: #fff; border: 2px solid #ff9800; }
    QStatusBar { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #232629, stop:1 #353941); color: #ff9800; font-weight: bold; font-size: 20px; border-bottom: 2px solid #0078d7; min-height: 48px; }
    QGroupBox { border: 2px solid #0078d7; border-radius: 16px; margin-top: 18px; background: #353941; color: #f0f0f0; box-shadow: 0 2px 8px rgba(0,0,0,0.10); }
    QGroupBox:title { subcontrol-origin: margin; left: 18px; padding: 0 6px 0 6px; font-size: 18px; font-weight: bold; }
    QPushButton { background-color: #0078d7; color: #fff; border-radius: 12px; padding: 10px 24px; font-size: 18px; font-weight: 600; box-shadow: 0 2px 8px rgba(0,0,0,0.10); }
    QPushButton:hover { background-color: #005fa3; box-shadow: 0 4px 16px rgba(0,120,215,0.15); }
    QPushButton:checked { background-color: #ff9800; color: #232629; border: 2px solid #0078d7; }
    QComboBox { background-color: #353941; color: #f0f0f0; border-radius: 12px; padding: 6px; font-size: 16px; }
    QSlider::groove:horizontal { height: 10px; background: #353941; border-radius: 5px; }
    QSlider::handle:horizontal { background: #0078d7; border: 2px solid #353941; width: 22px; margin: -6px 0; border-radius: 11px; }
    QLabel { font-size: 18px; }
    QVBoxLayout, QHBoxLayout { margin: 12px; }
    """
    app.setStyleSheet(dark_stylesheet)
    gui = FilamentDryerGUI()
    gui.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()