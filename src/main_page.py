import sys
import random
import datetime
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QSlider, QGridLayout, QGroupBox, QComboBox)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont
import pyqtgraph as pg
from src.pin_definitions import HEATER_PIN, FAN_PIN, TEMP_SENSOR_PIN, HUMIDITY_SENSOR_PIN, BUZZER_PIN, LED_PIN, BUTTON_PIN, PINS

class MainPage(QWidget):
    # Add heater and PWM state
    heater_on = False
    pwm_value = 0
    def update_presets(self, presets):
        self.presets = presets
        layout = self.layout()
        # Remove old preset card
        for i in range(layout.count()):
            item = layout.itemAt(i)
            widget = item.widget() if item is not None else None
            if isinstance(widget, QGroupBox) and widget.title() == 'Presets':
                layout.removeWidget(widget)
                widget.deleteLater()
                break
        # Recreate preset card
        preset_card = QGroupBox('Presets')
        preset_card.setStyleSheet('QGroupBox { border-radius: 16px; background: #353941; margin-top: 18px; } QGroupBox:title { font-size: 20px; font-weight: bold; color: #ff9800; }')
        preset_layout = QHBoxLayout()
        preset_label = QLabel('Preset:')
        preset_label.setFont(QFont('Segoe UI', 18, QFont.Weight.Bold))
        preset_layout.addWidget(preset_label)
        self.preset_buttons = {}
        for preset in self.presets:
            btn = QPushButton(preset)
            btn.setFont(QFont('Segoe UI', 18, QFont.Weight.Bold))
            btn.setCheckable(True)
            btn.setStyleSheet('QPushButton:checked { background-color: #ff9800; color: #232629; border: 2px solid #0078d7; }')
            btn.clicked.connect(lambda checked, p=preset: self.change_preset(p))
            self.preset_buttons[preset] = btn
            preset_layout.addWidget(btn)
        preset_card.setLayout(preset_layout)
        layout.insertWidget(0, preset_card)
    def start_dryer(self):
        print(f'Dryer started at {self.temperature_label.text()}')
        self.heater_on = True
        self.pwm_value = 255  # Example: full power
        self.timer_running = True
        self.countdown_timer.start(1000)

    def stop_dryer(self):
        print('Dryer stopped')
        self.heater_on = False
        self.pwm_value = 0
        self.timer_running = False
        self.countdown_timer.stop()
    switch_to_settings = pyqtSignal()
    
    def __init__(self):
        print("MainPage constructor called")
        super().__init__()
        self.selected_preset = "PLA"
        self.target_temperature = 34
        self.temperature_history = []
        self.humidity_history = []
        self.time_history = []
        # Preset data (should match settings_page)
        self.presets = {
            "PLA": {"temperature": 66, "drying_time": 60},
            "ABS": {"temperature": 59, "drying_time": 90},
            "PETG": {"temperature": 55, "drying_time": 75},
            "PC": {"temperature": 80, "drying_time": 120}
        }
        self.selected_preset = "PLA"
        self.target_temperature = self.presets[self.selected_preset]["temperature"]
        self.preset_time = self.presets[self.selected_preset]["drying_time"]
        self.remaining_time = self.preset_time * 60
        self.timer_running = False
        self.init_ui()
        self.simulate_timer = QTimer()
        self.simulate_timer.timeout.connect(self.simulate_environment)
        self.simulate_timer.start(1000)
        self.countdown_timer = QTimer()
        self.countdown_timer.timeout.connect(self.update_countdown)


    def init_ui(self):
        layout = QVBoxLayout()

        # Preset quick-select (buttons) in a rounded card
        preset_card = QGroupBox('Presets')
        preset_card.setStyleSheet('QGroupBox { border-radius: 16px; background: #353941; margin-top: 18px; box-shadow: 0 2px 8px rgba(0,0,0,0.10); } QGroupBox:title { font-size: 20px; font-weight: bold; color: #ff9800; }')
        preset_layout = QHBoxLayout()
        preset_label = QLabel('Preset:')
        preset_label.setFont(QFont('Segoe UI', 18, QFont.Weight.Bold))
        preset_layout.addWidget(preset_label)
        self.preset_buttons = {}
        for preset in self.presets:
            btn = QPushButton(preset)
            btn.setFont(QFont('Segoe UI', 18, QFont.Weight.Bold))
            btn.setCheckable(True)
            btn.setStyleSheet('QPushButton:checked { background-color: #ff9800; color: #232629; border: 2px solid #0078d7; }')
            btn.clicked.connect(lambda checked, p=preset: self.change_preset(p))
            self.preset_buttons[preset] = btn
        for btn in self.preset_buttons.values():
            preset_layout.addWidget(btn)
        preset_card.setLayout(preset_layout)
        layout.addWidget(preset_card)

        # Divider
        divider1 = QLabel()
        divider1.setFixedHeight(2)
        divider1.setStyleSheet('background: #0078d7; margin: 12px 0;')
        layout.addWidget(divider1)

        # Humidity label
        self.humidity_label = QLabel('Humidity: --%')
        self.humidity_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.humidity_label.setFont(QFont('Segoe UI', 18, QFont.Weight.Bold))
        layout.addWidget(self.humidity_label)

        # Temperature label (moved further down)
        self.temperature_label = QLabel('Temperature: 0°C')
        self.temperature_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.temperature_label.setFont(QFont('Segoe UI', 18, QFont.Weight.Bold))
        layout.addWidget(self.temperature_label)

        # Divider
        divider2 = QLabel()
        divider2.setFixedHeight(2)
        divider2.setStyleSheet('background: #0078d7; margin: 12px 0;')
        layout.addWidget(divider2)

        # Preset info and countdown
        self.preset_info_label = QLabel()
        self.preset_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preset_info_label.setFont(QFont('Segoe UI', 18, QFont.Weight.Bold))
        layout.addWidget(self.preset_info_label)

        self.countdown_label = QLabel()
        self.countdown_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.countdown_label.setFont(QFont('Segoe UI', 18, QFont.Weight.Bold))
        layout.addWidget(self.countdown_label)

        # Control buttons in a rounded card
        control_card = QGroupBox('Controls')
        control_card.setStyleSheet('QGroupBox { border-radius: 16px; background: #353941; margin-top: 18px; box-shadow: 0 2px 8px rgba(0,0,0,0.10); } QGroupBox:title { font-size: 20px; font-weight: bold; color: #ff9800; }')
        button_layout = QHBoxLayout()
        self.start_button = QPushButton('Start Dryer')
        self.start_button.setFont(QFont('Segoe UI', 18, QFont.Weight.Bold))
        self.start_button.clicked.connect(self.start_dryer)
        button_layout.addWidget(self.start_button)
        self.stop_button = QPushButton('Stop Dryer')
        self.stop_button.setFont(QFont('Segoe UI', 18, QFont.Weight.Bold))
        self.stop_button.clicked.connect(self.stop_dryer)
        button_layout.addWidget(self.stop_button)
        control_card.setLayout(button_layout)
        layout.addWidget(control_card)

        # Live graph (PyQtGraph) in a rounded card
        graph_group = QGroupBox("Live Environment Graph")
        graph_group.setStyleSheet('QGroupBox { border-radius: 16px; background: #353941; margin-top: 18px; box-shadow: 0 2px 8px rgba(0,0,0,0.10); } QGroupBox:title { font-size: 20px; font-weight: bold; color: #ff9800; }')
        graph_layout = QVBoxLayout()
        self.graph_widget = pg.PlotWidget()
        self.graph_widget.setBackground('w')
        self.graph_widget.showGrid(x=True, y=True)
        self.graph_widget.setMinimumHeight(250)
        self.temp_curve = self.graph_widget.plot(pen=pg.mkPen('r', width=2), name="Temperature (°C)")
        self.hum_curve = self.graph_widget.plot(pen=pg.mkPen('b', width=2), name="Humidity (%)")
        graph_layout.addWidget(self.graph_widget)
        graph_group.setLayout(graph_layout)
        layout.addWidget(graph_group)

        self.setLayout(layout)

    def update_selected_preset(self, preset):
        self.selected_preset = preset
        for p, btn in self.preset_buttons.items():
            if p == preset:
                btn.setChecked(True)
                btn.setStyleSheet('QPushButton { background-color: #0078d7; color: #fff; border: 2px solid #ff9800; }')
            else:
                btn.setChecked(False)
                btn.setStyleSheet('QPushButton { background-color: #353941; color: #f0f0f0; border: none; }')
        self.target_temperature = self.presets[preset]["temperature"]
        self.preset_time = self.presets[preset]["drying_time"]
        self.remaining_time = self.preset_time * 60
        self.update_preset_info()
        self.update_countdown_label()

    def change_preset(self, preset):
        self.update_selected_preset(preset)

    def simulate_environment(self):
        # Simulate temperature and humidity
        temp = 34 + random.uniform(-2, 2)
        humidity = 30 + random.uniform(-5, 5)
        self.temperature_label.setText(f'Temperature: {temp:.1f}°C')
        self.humidity_label.setText(f'Humidity: {humidity:.1f}%')
        self.temperature_history.append(temp)
        self.humidity_history.append(humidity)
        self.time_history.append(datetime.datetime.now().strftime('%H:%M:%S'))
        if len(self.temperature_history) > 60:
            self.temperature_history.pop(0)
            self.humidity_history.pop(0)
            self.time_history.pop(0)
        self.update_graph()

    def update_preset_info(self):
        preset = self.selected_preset
        temp = self.presets[preset]["temperature"]
        time = self.presets[preset]["drying_time"]
        self.preset_info_label.setText(f"Preset: {preset} | Temp: {temp}°C | Time: {time} min")

    def update_countdown_label(self):
        mins, secs = divmod(self.remaining_time, 60)
        self.countdown_label.setText(f"Time Remaining: {mins:02d}:{secs:02d}")

    def update_graph(self):
        # Use PyQtGraph for live plotting
        x = list(range(len(self.temperature_history)))
        self.temp_curve.setData(x, self.temperature_history)
        self.hum_curve.setData(x, self.humidity_history)

    def update_countdown(self):
        if self.timer_running and self.remaining_time > 0:
            self.remaining_time -= 1
            self.update_countdown_label()
            if self.remaining_time == 0:
                self.stop_dryer()

if __name__ == "__main__":
    print("Main entry point reached")
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = MainPage()
    window.show()
    sys.exit(app.exec())

