import os
import sys
import pytest
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import Qt
from .filament_dryer_gui import MyApp
def test_main_window(app):
    gui = MyApp()
    assert gui.isWidgetType(), "Failed to create main window"
