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

- Python 3.6+
- PyQt6

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python src/filament_dryer_gui.py
```

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