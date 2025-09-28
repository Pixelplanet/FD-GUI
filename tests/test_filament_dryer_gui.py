import pytest
from src.filament_dryer_gui import FilamentDryerGUI

def test_gui_initializes(qtbot):
    gui = FilamentDryerGUI()
    qtbot.addWidget(gui)
    assert gui.status_label.text().startswith("Temperature:")
    assert gui.time_label.text() == "" or ":" in gui.time_label.text()
    assert gui.led_label.isVisible()
