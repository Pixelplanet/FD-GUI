import pytest
from src.settings_page import SettingsPage

def test_add_preset(qtbot, tmp_path):
    file = tmp_path / "presets.json"
    page = SettingsPage(presets_file=str(file))
    page.presets = {}
    page.presets["TPU"] = {"temperature": 45, "drying_time": 80}
    page.save_presets()
    assert "TPU" in page.presets
    assert page.presets["TPU"]["drying_time"] == 80

def test_delete_preset(qtbot, tmp_path):
    file = tmp_path / "presets.json"
    page = SettingsPage(presets_file=str(file))
    page.presets = {"PLA": {"temperature": 34, "drying_time": 60}}
    page.save_presets()
    del page.presets["PLA"]
    page.save_presets()
    assert "PLA" not in page.presets
