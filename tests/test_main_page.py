import pytest
from src.main_page import MainPage

def test_main_page_initial_state(qtbot):
    page = MainPage()
    qtbot.addWidget(page)
    assert page.temperature_label.text().startswith("Temperature:")
    assert page.humidity_label.text().startswith("Humidity:")
    assert page.countdown_label.text().startswith("Time Remaining:")
    assert page.preset_info_label.text().startswith("Preset:")

def test_change_preset_updates_labels(qtbot):
    page = MainPage()
    qtbot.addWidget(page)
    page.change_preset("ABS")
    assert "ABS" in page.preset_info_label.text()
    assert page.target_temperature == page.presets["ABS"]["temperature"]
