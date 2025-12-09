# Filament Dryer GUI Project Documentation

This document provides a detailed description of the Filament Dryer GUI project, intended for developers who need to understand or rebuild the system.

## Project Overview

The project is a PyQt6-based graphical user interface for a filament dryer control system. It is designed to run on a Raspberry Pi (with a 7" touchscreen) but includes mock implementations for development on other platforms (Windows/Linux).

### Directory Structure

-   `filament_dryer_gui.py`: The main entry point of the application.
-   `src/`: Contains the source code for individual pages and logic.
    -   `main_page.py`: The primary dashboard.
    -   `settings_page.py`: Configuration for presets and PID control.
    -   `debugging_page.py`: Diagnostic view of internal state.
    -   `testing_page.py`: Standalone hardware testing utility.
    -   `preset_selection_page.py`: (Likely legacy/alternative) Standalone preset selector.
    -   `pin_definitions.py`: GPIO pin mappings.
-   `presets.json`: JSON file storing filament presets.

## Entry Point: `filament_dryer_gui.py`

This file sets up the main application window (`FilamentDryerGUI`).

-   **Window Setup**: Configures the window for full-screen mode (suitable for touchscreens).
-   **Navigation**: Uses a `QTabWidget` to switch between "Main", "Settings", and "Debug" tabs.
-   **Status Bar**: Displays real-time information (Temperature, Humidity, Status, Preset, Time Remaining) and a system clock. It also shows a simulated LED indicator for heater status.
-   **Inter-Page Communication**: Connects signals between pages (e.g., updating presets on the Main Page when changed in Settings).
-   **Theme**: Applies a dark, modern stylesheet (Segoe UI font, dark grey backgrounds, blue/orange accents).

## Page Functionality

### 1. Main Page (`src/main_page.py`)

The `MainPage` is the operational dashboard.

-   **Presets**: Displays a list of available filament presets (e.g., PLA, ABS) as buttons. Selecting a preset updates the target temperature and drying time.
-   **Environment Monitoring**: Shows current Temperature and Humidity.
-   **Controls**:
    -   **Start Dryer**: Activates the heater (sets `heater_on` flag, starts PWM simulation).
    -   **Stop Dryer**: Deactivates the heater.
-   **Countdown**: Displays remaining drying time.
-   **Graph**: A live `pyqtgraph` plot showing Temperature and Humidity history.
-   **Simulation**: If no hardware is present, it simulates environment data (random fluctuations) and heater response.

### 2. Settings Page (`src/settings_page.py`)

The `SettingsPage` handles configuration and data management.

-   **Preset Management**:
    -   **View**: Grid view of existing presets.
    -   **Add**: Dialog to create new presets (Name, Temp, Time). Includes an On-Screen Keyboard (OSK) trigger for Raspberry Pi.
    -   **Edit**: Dialog to modify or delete existing presets.
    -   **Storage**: Loads from and saves to `presets.json`.
-   **PID Control**:
    -   **Configuration**: Fields to set P, I, and D values for the heater controller.
    -   **Auto-Tune**: A simulated PID auto-tune routine that estimates parameters based on a simulated step response.

### 3. Debugging Page (`src/debugging_page.py`)

The `DebuggingPage` provides a read-only view of the system's internal state.

-   **State Inspection**: Displays values from `MainPage` (current preset, target temp, history) and `SettingsPage` (loaded presets).
-   **Refresh**: Button to manually update the displayed information (also updates automatically via timer).

### 4. Testing Page (`src/testing_page.py`)

A standalone utility for hardware verification.

-   **Hardware Abstraction**: Includes `MockGPIO` and `MockPWM` classes to run without actual Raspberry Pi GPIO.
-   **Manual Control**:
    -   **Target Temp**: Set a specific target temperature.
    -   **Control Toggle**: Enable/Disable the simulated temperature control loop.
-   **Feedback**: Shows current temperature, heating status (ON/OFF), and PWM duty cycle.

### 5. Preset Selection Page (`src/preset_selection_page.py`)

*Note: This appears to be a standalone or alternative implementation not currently used in the main tabbed interface.*

-   **Functionality**: Allows selecting a preset to return to a main view (via signal) and editing presets.
-   **UI**: Grid of preset buttons and an "Edit Presets" dialog with sliders.

## Data Storage

-   **`presets.json`**: Stores filament presets.
    -   Format: `{"PresetName": {"temperature": int, "drying_time": int}}`
    -   The system handles migration from older formats if necessary.

## Hardware Interface

-   **`src/pin_definitions.py`**: Defines GPIO pin numbers for Heater, Fan, Sensors, Buzzer, LED, and Buttons.
-   **GPIO Handling**: The code checks for `RPi.GPIO`. If unavailable (e.g., on Windows), it falls back to mock implementations to allow GUI development and testing.

## Rebuilding Instructions

To rebuild this system:
1.  **Dependencies**: Install `PyQt6` and `pyqtgraph`.
2.  **Structure**: Recreate the `src` directory and place the page classes there.
3.  **Entry**: Create the main `QMainWindow` to host the pages in a `QTabWidget`.
4.  **Logic**: Implement the signal/slot connections for navigation and data updates (especially between Settings and Main).
5.  **Hardware**: Implement the GPIO logic (or mocks) for heater control and sensor reading.
