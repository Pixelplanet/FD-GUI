import pytest
import json
import os
from src.settings_page import SettingsPage

@pytest.fixture
def presets_file(tmp_path):
    file = tmp_path / "presets.json"
    file.write_text(json.dumps({
        "PLA": {"temperature": 34, "drying_time": 60},
        "ABS": {"temperature": 69, "drying_time": 120}
    }))
    return str(file)

def test_load_presets_valid(qtbot, presets_file):
    page = SettingsPage(presets_file=presets_file)
    assert "PLA" in page.presets
    assert page.presets["PLA"]["temperature"] == 34
    assert page.presets["ABS"]["drying_time"] == 120

def test_save_presets(tmp_path, qtbot):
    file = tmp_path / "presets.json"
    page = SettingsPage(presets_file=str(file))
    page.presets = {"PETG": {"temperature": 55, "drying_time": 90}}
    page.save_presets()
    data = json.loads(file.read_text())
    assert "PETG" in data
    assert data["PETG"]["temperature"] == 55
