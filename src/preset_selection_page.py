import sys
import json
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, 
                             QPushButton, QGridLayout, QDialog, QDialogButtonBox,
                             QSlider, QHBoxLayout, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

class PresetSelectionPage(QWidget):
    switch_to_main = pyqtSignal(str)
    
    def __init__(self, presets_file='presets.json'):
        super().__init__()
        self.presets_file = presets_file
        self.presets = self.load_presets()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title_label = QLabel('Preset Selection')
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont('Arial', 24, QFont.Weight.Bold))
        layout.addWidget(title_label)
        
        # Preset buttons grid
        grid_layout = QGridLayout()
        
        row = 0
        col = 0
        for i, (preset, value) in enumerate(self.presets.items()):
            button = QPushButton(f'{preset}\n{value}')
            button.setFont(QFont('Arial', 16, QFont.Weight.Bold))
            button.setFixedSize(150, 100)
            # Store the preset name with the button for reference
            button.preset_name = preset
            button.clicked.connect(lambda checked, btn=button: self.select_preset(btn.preset_name))
            
            grid_layout.addWidget(button, row, col)
            
            col += 1
            if col > 2:  # 3 columns
                col = 0
                row += 1
                
        layout.addLayout(grid_layout)
        
        # Edit button
        edit_layout = QHBoxLayout()
        self.edit_button = QPushButton('Edit Presets')
        self.edit_button.setFont(QFont('Arial', 14))
        self.edit_button.clicked.connect(self.open_edit_presets_dialog)
        edit_layout.addWidget(self.edit_button)
        
        layout.addLayout(edit_layout)
        
        # Back button
        self.back_button = QPushButton('Back to Main')
        self.back_button.setFont(QFont('Arial', 14))
        self.back_button.clicked.connect(lambda: self.switch_to_main.emit(None))
        layout.addWidget(self.back_button)
        
        self.setLayout(layout)
        
    def load_presets(self):
        try:
            with open(self.presets_file, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                'PLA': '34°C',
                'ABS': '69°C', 
                'PETG': '55°C'
            }
            
    def select_preset(self, preset_name):
        """Select a preset and return to main page"""
        print(f"Selected preset: {preset_name} with value {self.presets[preset_name]}")
        self.switch_to_main.emit(preset_name)
        
    def open_edit_presets_dialog(self):
        # Create popup dialog for editing presets
        dialog = QDialog(self)
        dialog.setWindowTitle('Edit Presets')
        dialog.setModal(True)
        dialog.resize(500, 400)
        
        layout = QVBoxLayout()
        
        # Title
        title_label = QLabel('Edit Preset Values')
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont('Arial', 18, QFont.Weight.Bold))
        layout.addWidget(title_label)
        
        # Grid for preset editing
        grid_layout = QGridLayout()
        
        self.preset_edit_widgets = {}
        
        for i, (preset, value) in enumerate(self.presets.items()):
            label = QLabel(f'{preset}:')
            label.setFont(QFont('Arial', 14))
            
            # Create slider for temperature
            slider = QSlider(Qt.Orientation.Horizontal)
            slider.setMinimum(0)
            slider.setMaximum(100)
            slider.setValue(int(value.replace('°C', '')))
            
            # Value display label
            value_label = QLabel(f'{slider.value()}°C')
            value_label.setFont(QFont('Arial', 12))
            
            def create_slider_change_handler(preset_name, value_label):
                def handler(value):
                    value_label.setText(f'{value}°C')
                return handler
            
            slider.valueChanged.connect(create_slider_change_handler(preset, value_label))
            
            # Store references for saving
            self.preset_edit_widgets[preset] = {
                'slider': slider,
                'value_label': value_label
            }
            
            grid_layout.addWidget(label, i, 0)
            grid_layout.addWidget(slider, i, 1)
            grid_layout.addWidget(value_label, i, 2)
            
        layout.addLayout(grid_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        save_button = QPushButton('Save Changes')
        save_button.setFont(QFont('Arial', 14))
        save_button.clicked.connect(lambda: self.save_edited_presets(dialog))
        
        cancel_button = QPushButton('Cancel')
        cancel_button.setFont(QFont('Arial', 14))
        cancel_button.clicked.connect(dialog.reject)
        
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
        
        dialog.setLayout(layout)
        dialog.exec()
        
    def save_edited_presets(self, dialog):
        # Update presets with new values
        for preset_name, widgets in self.preset_edit_widgets.items():
            value = f'{widgets["slider"].value()}°C'
            self.presets[preset_name] = value
            
        # Save to file
        try:
            with open(self.presets_file, 'w') as file:
                json.dump(self.presets, file)
            QMessageBox.information(self, 'Success', 'Presets saved successfully!')
            print('Presets saved:', self.presets)
            dialog.accept()
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to save presets: {str(e)}')
            print(f'Failed to save presets: {e}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    preset_page = PresetSelectionPage()
    preset_page.show()
    sys.exit(app.exec())
