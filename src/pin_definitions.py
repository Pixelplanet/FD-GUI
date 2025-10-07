# pin_definitions.py
# Centralized pin definitions for Raspberry Pi GPIO and related hardware

# Example pin assignments (customize as needed)
HEATER_PIN = 18
FAN_PIN = 17
TEMP_SENSOR_PIN = 4
HUMIDITY_SENSOR_PIN = 5
#BUZZER_PIN = 22
#LED_PIN = 27
#BUTTON_PIN = 23
# Add more pins as needed

# You can also use a dictionary for grouped pins
PINS = {
    'heater': HEATER_PIN,
    'fan': FAN_PIN,
    'temp_sensor': TEMP_SENSOR_PIN,
    'humidity_sensor': HUMIDITY_SENSOR_PIN,
    'buzzer': BUZZER_PIN,
    'led': LED_PIN,
    'button': BUTTON_PIN,
}
