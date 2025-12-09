# Filament Dryer Control System

A PyQt6-based GUI application for controlling a filament dryer system, designed to run on both Windows and Raspberry Pi with a 7" touchscreen.

## Features

- Main control interface with temperature slider
- Preset selection for common drying profiles
- Settings configuration page
- Testing mode for system validation
- Full-screen interface optimized for 7" touchscreen
- Cross-platform compatibility (Windows/Raspberry Pi)

## Requirements

- Python 3.8+ (system Python on Raspberry Pi Bookworm is 3.11)
- The GUI framework is provided by PyQt6 on desktop development environments. On Raspberry Pi, install the system PyQt package via apt (see notes below).

## Installation (Desktop)

1. Create and activate a virtual environment (recommended):
```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install the Python packages (note: PyQt is not included in requirements for Raspberry Pi compatibility):
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python -m src.filament_dryer_gui
```

## Raspberry Pi (recommended approach)

Building PyQt from pip on Raspberry Pi often fails because wheels are not available for all Python versions/architectures. Use the system package for PyQt instead:

```bash
# Update package lists
sudo apt update

# Install system PyQt5 (works with system Python)
sudo apt install python3-pyqt5

# Create a virtualenv (optional) and activate it
python3 -m venv .venv
source .venv/bin/activate

# Install other Python deps from requirements.txt (PyQt removed from requirements)
pip install -r requirements.txt
```

Notes:
- If you need an isolated venv with a specific Python version, consider installing a compatible Python (3.9) or build from source — both are advanced options and not required for most users.
- On Raspberry Pi OS, using `python3-pyqt5` from apt is the fastest, most reliable option.

## Usage

The application consists of four main pages:

1. **Main Page**: Control the dryer with temperature slider and start/stop buttons
2. **Preset Selection**: Choose from predefined drying profiles
3. **Settings**: Configure system parameters
4. **Testing Mode**: Run test cycles to validate system functionality

## Project Structure

```
src/
├── filament_dryer_gui.py    # Main application entry point
├── main_page.py             # Main control interface
├── preset_selection_page.py # Preset selection page
├── settings_page.py         # Settings configuration
└── testing_page.py          # Testing mode interface
```

## Hardware Integration

The GUI is designed to be easily integrated with hardware components:
- Temperature sensors for monitoring
- Heating elements for temperature control
- Relay modules for switching
- Touchscreen display (7")

## Cross-Platform Compatibility

The application uses PyQt6 which provides consistent behavior across:
- Windows 10/11 desktops
- Raspberry Pi with touchscreen displays
- Other Linux-based systems

## Customization

To extend the functionality:
1. Modify individual page files to add new features
2. Add hardware integration code in the main application file
3. Update presets in `preset_selection_page.py`
4. Adjust styling in individual page files

## License

This project is licensed under the MIT License - see the LICENSE file for details.