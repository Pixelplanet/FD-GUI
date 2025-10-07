import sys
import time
import threading
from collections import deque
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QSlider, QGroupBox, 
                             QGridLayout, QFrame, QLineEdit)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from src.pin_definitions import HEATER_PIN, FAN_PIN, TEMP_SENSOR_PIN, HUMIDITY_SENSOR_PIN, BUZZER_PIN, LED_PIN, BUTTON_PIN, PINS
from PyQt6.QtGui import QFont

# GPIO mock and detection
def is_raspberry_pi():
    try:
        with open('/proc/cpuinfo', 'r') as f:
            cpuinfo = f.read()
            return 'Raspberry Pi' in cpuinfo or 'BCM' in cpuinfo
    except Exception:
        return False

class MockPWM:
    def __init__(self, pin, frequency):
        self.pin = pin
        self.frequency = frequency
        self.duty_cycle = 0
        self.is_running = False
    def start(self, duty_cycle):
        self.duty_cycle = duty_cycle
        self.is_running = True
    def ChangeDutyCycle(self, duty_cycle):
        self.duty_cycle = duty_cycle
    def stop(self):
        self.is_running = False

class MockGPIO:
    def __init__(self):
        self.PWM = MockPWM
        self.BCM = "BCM"
        self.OUT = "OUT"
        self.IN = "IN"
        self.PUD_UP = "PUD_UP"
    def setmode(self, mode):
        pass
    def setup(self, pin, mode, pull_up_down=None):
        pass
    def PWM(self, pin, frequency):
        return MockPWM(pin, frequency)

try:
    import RPi.GPIO as GPIO
    GPIO_AVAILABLE = True
except ImportError:
    GPIO = MockGPIO()
    GPIO_AVAILABLE = False

class TestingPage(QWidget):
    switch_to_main = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.pwm = None
        self.target_temperature = 0
        self.current_temperature = 25.0  # Default room temperature
        self.temperature_control_active = False
        self.stop_temp_thread = False
        
        # Data storage for graphing
        self.temp_history = deque(maxlen=120)
        self.pwm_history = deque(maxlen=120)
        self.time_history = deque(maxlen=120)
        
        self.init_ui()
        
        # Start temperature monitoring thread if GPIO is available
        if GPIO_AVAILABLE:
            self.temp_thread = threading.Thread(target=self.update_temperature, daemon=True)
            self.temp_thread.start()
            
    def init_ui(self):
        layout = QVBoxLayout()
        def init_ui(self):
            layout = QVBoxLayout()

            # Title
            title_label = QLabel('Testing Mode')
            title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            title_label.setFont(QFont('Arial', 24, QFont.Weight.Bold))
            layout.addWidget(title_label)

            # Temperature display group
            temp_group = QGroupBox("Temperature Readout")
            temp_layout = QVBoxLayout()

            self.temp_label = QLabel('Temperature: -- °C')
            self.temp_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.temp_label.setFont(QFont('Arial', 16))
            temp_layout.addWidget(self.temp_label)
            temp_group.setLayout(temp_layout)
                    # Pin assignments from pin_definitions
                    self.heater_pin = HEATER_PIN
                    self.fan_pin = FAN_PIN
                    self.temp_sensor_pin = TEMP_SENSOR_PIN
                    self.humidity_sensor_pin = HUMIDITY_SENSOR_PIN
                    self.buzzer_pin = BUZZER_PIN
                    self.led_pin = LED_PIN
                    self.button_pin = BUTTON_PIN
                    self.pins = PINS
            layout.addWidget(temp_group)

            # Target temperature input
            target_group = QGroupBox("Target Temperature")
            target_layout = QVBoxLayout()

            self.target_temp_label = QLabel('Target Temperature (°C):')
            self.target_temp_label.setFont(QFont('Arial', 14))
            target_layout.addWidget(self.target_temp_label)

            self.target_temp_input = QLineEdit()
            self.target_temp_input.setPlaceholderText("Enter target temperature")
            self.target_temp_input.setFont(QFont('Arial', 12))
            target_layout.addWidget(self.target_temp_input)

            self.set_target_btn = QPushButton('Set Target')
            self.set_target_btn.setFont(QFont('Arial', 14))
            self.set_target_btn.clicked.connect(self.set_target_temperature)
            target_layout.addWidget(self.set_target_btn)

            target_group.setLayout(target_layout)
            layout.addWidget(target_group)

            # Control toggle
            control_layout = QHBoxLayout()

            self.temp_control_btn = QPushButton('Enable Temp Control')
            self.temp_control_btn.setFont(QFont('Arial', 14))
            self.temp_control_btn.clicked.connect(self.toggle_temp_control)
            control_layout.addWidget(self.temp_control_btn)

            layout.addLayout(control_layout)

            # Status indicators
            status_group = QGroupBox("System Status")
            status_layout = QVBoxLayout()

            self.heating_label = QLabel('Heating: OFF')
            self.heating_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.heating_label.setFont(QFont('Arial', 14))
            status_layout.addWidget(self.heating_label)

            self.pwm_value_label = QLabel('PWM: 0%')
            self.pwm_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.pwm_value_label.setFont(QFont('Arial', 14))
            status_layout.addWidget(self.pwm_value_label)

            status_group.setLayout(status_layout)
            layout.addWidget(status_group)

            # Back button
            self.back_btn = QPushButton('Back')
            self.back_btn.setFont(QFont('Arial', 14))
            self.back_btn.clicked.connect(self.switch_to_main.emit)
            layout.addWidget(self.back_btn)

            self.setLayout(layout)

            # Start update timer for UI
            self.update_timer = QTimer()
            self.update_timer.timeout.connect(self.update_ui)
            self.update_timer.start(1000)  # Update every second
        
    def set_target_temperature(self):
        try:
            temp = float(self.target_temp_input.text())
            self.target_temperature = temp
            self.target_temp_label.setText(f"Target Temperature (°C): {self.target_temperature:.2f}")
        except ValueError:
            self.target_temp_label.setText("Target Temperature (°C): Invalid input")
            
    def toggle_temp_control(self):
        self.temperature_control_active = not self.temperature_control_active
        if self.temperature_control_active:
            self.temp_control_btn.setText("Disable Temp Control")
        else:
            self.temp_control_btn.setText("Enable Temp Control")
            
    def update_temperature(self):
        """Simulate temperature reading (only on Raspberry Pi)"""
        # In a real implementation, this would read from the actual sensor
        while not self.stop_temp_thread:
            if GPIO_AVAILABLE:
                # On Raspberry Pi, we'd read from 1-Wire sensor
                # For now we'll simulate some realistic temperature changes
                pass
            
            # Simulate temperature changes for demo purposes
            time.sleep(1)
            
    def update_ui(self):
        """Update UI elements with current values"""
        # Update temperature display (simulate with random fluctuation)
        import random
        if self.temperature_control_active and self.target_temperature > 0:
            # Simulate heating towards target
            if self.current_temperature < self.target_temperature:
                self.current_temperature += random.uniform(0.1, 0.5)
            elif self.current_temperature > self.target_temperature:
                self.current_temperature -= random.uniform(0.1, 0.3)
                
        # Keep within realistic bounds
        self.current_temperature = max(20, min(100, self.current_temperature))
        
        self.temp_label.setText(f"Temperature: {self.current_temperature:.2f} °C")
        
        # Simulate PWM control for demo purposes
        if self.temperature_control_active and self.target_temperature > 0:
            error = self.target_temperature - self.current_temperature
            if error > 0:
                if error > 5:
                    pwm_value = 100
                elif error > 2:
                    pwm_value = 60
                elif error > 0.5:
                    pwm_value = 30
                else:
                    pwm_value = 10
                self.heating_label.setText('Heating: ON')
            else:
                pwm_value = 0
                self.heating_label.setText('Heating: OFF')
        else:
            pwm_value = 0
            self.heating_label.setText('Heating: OFF')
            
        self.pwm_value_label.setText(f'PWM: {pwm_value}%')
        
        # Update history for graphing (simulated)
        current_time = time.time()
        self.temp_history.append(self.current_temperature)
        self.pwm_history.append(pwm_value)
        self.time_history.append(current_time)
        
    def closeEvent(self, event):
        """Handle window closing"""
        self.stop_temp_thread = True
        if GPIO_AVAILABLE and self.pwm:
            self.pwm.stop()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    testing_page = TestingPage()
    testing_page.show()
    sys.exit(app.exec_())