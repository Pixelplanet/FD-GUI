"""Non-blocking smoke test for the Filament Dryer GUI.
This script launches the GUI, programmatically switches tabs, exercises a few
non-blocking methods (start/stop dryer, simulate_environment, update_top_bar),
then quits. It avoids opening modal dialogs so it can run unattended.
"""
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from src.filament_dryer_gui import FilamentDryerGUI


def run_smoke_test():
    app = QApplication(sys.argv)
    gui = FilamentDryerGUI()
    gui.show()

    # Sequence of actions (timed) to exercise main flows without modal dialogs
    def step_switch_to_settings():
        try:
            gui.tabs.setCurrentWidget(gui.settings_page)
            print('Switched to Settings tab')
        except Exception as e:
            print('Error switching to Settings:', e)

    def step_switch_to_debug():
        try:
            gui.tabs.setCurrentWidget(gui.debugging_page)
            print('Switched to Debug tab')
        except Exception as e:
            print('Error switching to Debug:', e)

    def step_switch_to_main():
        try:
            gui.tabs.setCurrentWidget(gui.main_page)
            print('Switched to Main tab')
        except Exception as e:
            print('Error switching to Main:', e)

    def step_start_stop():
        try:
            gui.main_page.start_dryer()
            print('Started dryer')
            QTimer.singleShot(300, lambda: (gui.main_page.stop_dryer(), print('Stopped dryer')))
        except Exception as e:
            print('Error starting/stopping dryer:', e)

    def step_simulate_and_update():
        try:
            gui.main_page.simulate_environment()
            print('Simulated environment')
            gui.update_top_bar()
            print('Updated top bar')
        except Exception as e:
            print('Error simulating environment or updating top bar:', e)

    # Schedule steps
    QTimer.singleShot(200, step_switch_to_settings)
    QTimer.singleShot(600, step_switch_to_debug)
    QTimer.singleShot(1000, step_switch_to_main)
    QTimer.singleShot(1400, step_start_stop)
    QTimer.singleShot(2000, step_simulate_and_update)

    # Quit after the interactions
    QTimer.singleShot(2600, lambda: (print('Smoke test finished, quitting.'), app.quit()))

    sys.exit(app.exec())


if __name__ == '__main__':
    run_smoke_test()
