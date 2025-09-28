import sys
import json
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, 
                             QPushButton, QGridLayout, QDialog, QDialogButtonBox,
                             QSlider, QLineEdit, QHBoxLayout, QMessageBox, QGroupBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

class SettingsPage(QWidget):
    presets_changed = pyqtSignal(dict)
    def open_add_preset_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle('Add New Preset')
        dialog.setModal(True)
        layout = QVBoxLayout()
        name_edit = QLineEdit()
        temp_edit = QLineEdit()
        time_edit = QLineEdit()
        name_edit.setPlaceholderText('Preset Name')
        temp_edit.setPlaceholderText('Temperature (°C)')
        time_edit.setPlaceholderText('Drying Time (min)')
        layout.addWidget(QLabel('Preset Name:'))
        layout.addWidget(name_edit)
        layout.addWidget(QLabel('Temperature (°C):'))
        layout.addWidget(temp_edit)
        layout.addWidget(QLabel('Drying Time (min):'))
        layout.addWidget(time_edit)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        def accept():
            name = name_edit.text().strip()
            try:
                temp = int(temp_edit.text().strip())
                time = int(time_edit.text().strip())
            except ValueError:
                QMessageBox.warning(self, 'Input Error', 'Temperature and drying time must be numbers.')
                return
            if not name:
                QMessageBox.warning(self, 'Input Error', 'Preset name required.')
                return
            if name in self.presets:
                QMessageBox.warning(self, 'Duplicate', 'Preset already exists.')
                return
            self.presets[name] = {'temperature': temp, 'drying_time': time}
            self.save_presets()
            self.refresh_presets_grid()
            self.presets_changed.emit(self.presets)
            dialog.accept()
        button_box.accepted.connect(accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        dialog.setLayout(layout)
        dialog.exec()
    def open_edit_preset_dialog(self, preset):
        data = self.presets[preset]
        dialog = QDialog(self)
        dialog.setWindowTitle(f'Edit Preset: {preset}')
        dialog.setModal(True)
        layout = QVBoxLayout()

        name_edit = QLineEdit(preset)
        temp_edit = QLineEdit(str(data.get('temperature', '')))
        time_edit = QLineEdit(str(data.get('drying_time', '')))
        name_edit.setPlaceholderText('Preset Name')
        temp_edit.setPlaceholderText('Temperature (°C)')
        time_edit.setPlaceholderText('Drying Time (min)')
        layout.addWidget(QLabel('Preset Name:'))
        layout.addWidget(name_edit)
        layout.addWidget(QLabel('Temperature (°C):'))
        layout.addWidget(temp_edit)
        layout.addWidget(QLabel('Drying Time (min):'))
        layout.addWidget(time_edit)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        delete_btn = QPushButton('Delete')
        delete_btn.setStyleSheet('background-color: #d32f2f; color: #fff; font-weight: bold; border-radius: 8px; padding: 6px 12px;')
        def accept():
            name = name_edit.text().strip()
            try:
                temp = int(temp_edit.text().strip())
                time = int(time_edit.text().strip())
            except ValueError:
                QMessageBox.warning(self, 'Input Error', 'Temperature and drying time must be numbers.')
                return
            if not name:
                QMessageBox.warning(self, 'Input Error', 'Preset name required.')
                return
            # Remove old if renamed
            if name != preset:
                del self.presets[preset]
            self.presets[name] = {'temperature': temp, 'drying_time': time}
            self.save_presets()
            self.refresh_presets_grid()
            self.presets_changed.emit(self.presets)
            dialog.accept()
        def delete():
            reply = QMessageBox.question(dialog, 'Delete Preset', f'Are you sure you want to delete preset "{preset}"?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                if preset in self.presets:
                    del self.presets[preset]
                    # Only save and refresh if there are presets left and dict is valid
                    if self.presets and isinstance(self.presets, dict):
                        self.save_presets()
                        self.refresh_presets_grid()
                        self.presets_changed.emit(self.presets)
                dialog.accept()
        button_box.accepted.connect(accept)
        button_box.rejected.connect(dialog.reject)
        delete_btn.clicked.connect(delete)
        layout.addWidget(button_box)
        layout.addWidget(delete_btn)
        dialog.setLayout(layout)
        dialog.exec()
    switch_to_main = pyqtSignal()
    
    def __init__(self, presets_file='presets.json'):
        super().__init__()
        self.presets_file = presets_file
        self.presets = self.load_presets()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()

        # Title
        title_label = QLabel('Preset Selection & Settings')
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont('Segoe UI', 24, QFont.Weight.Bold))
        layout.addWidget(title_label)

        # Divider
        divider1 = QLabel()
        divider1.setFixedHeight(2)
        divider1.setStyleSheet('background: #0078d7; margin: 12px 0;')
        layout.addWidget(divider1)

        # Preset buttons grid in a rounded card
        preset_card = QGroupBox('Presets')
        preset_card.setStyleSheet('QGroupBox { border-radius: 16px; background: #353941; margin-top: 18px; box-shadow: 0 2px 8px rgba(0,0,0,0.10); } QGroupBox:title { font-size: 20px; font-weight: bold; color: #ff9800; }')
        preset_card_layout = QVBoxLayout()
        self.grid_layout = QGridLayout()
        self.preset_buttons = {}
        self.preset_labels = {}
        self.refresh_presets_grid()
        preset_card_layout.addLayout(self.grid_layout)
        preset_card_layout.addStretch()
        add_layout = QHBoxLayout()
        plus_btn = QPushButton('+')
        plus_btn.setFont(QFont('Segoe UI', 24, QFont.Weight.Bold))
        plus_btn.setFixedSize(40, 40)
        plus_btn.setStyleSheet('background-color: #0078d7; color: #fff; border-radius: 20px;')
        plus_btn.clicked.connect(self.open_add_preset_dialog)
        add_layout.addStretch()
        add_layout.addWidget(plus_btn)
        preset_card_layout.addLayout(add_layout)
        preset_card.setLayout(preset_card_layout)
        layout.addWidget(preset_card)

        # Divider
        divider2 = QLabel()
        divider2.setFixedHeight(2)
        divider2.setStyleSheet('background: #0078d7; margin: 12px 0;')
        layout.addWidget(divider2)

        # Collapsible PID Controls Section
        from PyQt6.QtWidgets import QToolButton
        pid_group = QGroupBox('PID Heater Control')
        pid_group.setStyleSheet('QGroupBox { border-radius: 16px; background: #353941; margin-top: 18px; box-shadow: 0 2px 8px rgba(0,0,0,0.10); } QGroupBox:title { font-size: 20px; font-weight: bold; color: #ff9800; }')
        pid_layout = QVBoxLayout()
        pid_desc = QLabel('Adjust PID values for PWM heater control to minimize overshoot and hysteresis.')
        pid_desc.setWordWrap(True)
        pid_layout.addWidget(pid_desc)

        self.pid_p_edit = QLineEdit()
        self.pid_i_edit = QLineEdit()
        self.pid_d_edit = QLineEdit()
        self.pid_p_edit.setPlaceholderText('P (Proportional)')
        self.pid_i_edit.setPlaceholderText('I (Integral)')
        self.pid_d_edit.setPlaceholderText('D (Derivative)')
        pid_layout.addWidget(QLabel('P:'))
        pid_layout.addWidget(self.pid_p_edit)
        pid_layout.addWidget(QLabel('I:'))
        pid_layout.addWidget(self.pid_i_edit)
        pid_layout.addWidget(QLabel('D:'))
        pid_layout.addWidget(self.pid_d_edit)

        pid_save_btn = QPushButton('Save PID Values')
        pid_save_btn.setFont(QFont('Segoe UI', 18, QFont.Weight.Bold))
        pid_save_btn.setStyleSheet('background-color: #0078d7; color: #fff; border-radius: 12px; padding: 10px 24px; font-size: 18px; font-weight: 600; box-shadow: 0 2px 8px rgba(0,0,0,0.10);')
        pid_save_btn.clicked.connect(self.save_pid_values)
        pid_layout.addWidget(pid_save_btn)

        # Collapsible button
        collapse_btn = QToolButton()
        collapse_btn.setText('▼')
        collapse_btn.setStyleSheet('font-size: 18px; color: #ff9800; background: transparent; border: none;')
        collapse_btn.setCheckable(True)
        collapse_btn.setChecked(True)
        def toggle_pid():
            pid_group.setVisible(collapse_btn.isChecked())
            collapse_btn.setText('▼' if collapse_btn.isChecked() else '▲')
        collapse_btn.toggled.connect(toggle_pid)
        layout.addWidget(collapse_btn)
        pid_group.setLayout(pid_layout)
        layout.addWidget(pid_group)
        self.setLayout(layout)
    def save_pid_values(self):
        try:
            p = float(self.pid_p_edit.text())
            i = float(self.pid_i_edit.text())
            d = float(self.pid_d_edit.text())
            self.pid_values = {'P': p, 'I': i, 'D': d}
            QMessageBox.information(self, 'PID Saved', f'PID values saved: P={p}, I={i}, D={d}')
        except ValueError:
            QMessageBox.warning(self, 'Input Error', 'PID values must be numbers.')
    def refresh_presets_grid(self):
        # Clear grid
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                self.grid_layout.removeWidget(widget)
                widget.deleteLater()
        self.preset_buttons.clear()
        self.preset_labels.clear()
        # Sort presets top-down
        presets_sorted = sorted(self.presets.keys())
        for idx, preset in enumerate(presets_sorted):
            data = self.presets[preset]
            label = QLabel(f'{preset}:')
            label.setFont(QFont('Arial', 14))
            self.preset_labels[preset] = label
            # Ensure btn_text is always a string
            temp = data.get('temperature', '')
            time = data.get('drying_time', '')
            btn_text = f"{temp}°C, {time} min"
            button = QPushButton(str(btn_text))
            button.setFont(QFont('Arial', 16, QFont.Weight.Bold))
            button.setFixedSize(120, 40)
            import functools
            button.clicked.connect(functools.partial(self.open_edit_preset_dialog, preset))
            self.preset_buttons[preset] = button
            row = idx // 2
            col = (idx % 2) * 2
            self.grid_layout.addWidget(label, row, col)
            self.grid_layout.addWidget(button, row, col + 1)

        # Modern style for grid
        self.grid_layout.setSpacing(10)
        self.grid_layout.setContentsMargins(20, 10, 20, 10)
        self.setStyleSheet('QLabel { font-size: 16px; } QPushButton { font-size: 16px; padding: 6px 12px; border-radius: 8px; background-color: #0078d7; color: #fff; } QPushButton:hover { background-color: #005fa3; } QLineEdit { font-size: 16px; border-radius: 8px; padding: 4px; }')
        
    def load_presets(self):
        try:
            with open(self.presets_file, 'r') as file:
                data = json.load(file)
            # Migrate old format if needed
            migrated = {}
            for k, v in data.items():
                if isinstance(v, dict):
                    migrated[k] = v
                else:
                    migrated[k] = {
                        'temperature': int(str(v).replace('°C','')), 
                        'drying_time': 60
                    }
            return migrated
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                'PLA': {'temperature': 34, 'drying_time': 60},
                'ABS': {'temperature': 69, 'drying_time': 120},
                'PETG': {'temperature': 55, 'drying_time': 90}
            }
            
    def open_slider_popup(self, preset):
        dialog = QDialog(self)
        dialog.setWindowTitle(f'Set {preset}')
        dialog.setModal(True)

        layout = QVBoxLayout()

        # Slider for temperature
        slider_layout = QHBoxLayout()
        slider_label = QLabel('Temperature:')
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(100)
        slider.setValue(int(self.presets[preset]['temperature']))

        value_label = QLabel(f'{slider.value()}°C')
        value_label.setFont(QFont('Arial', 12))

        def update_slider_label(value):
            value_label.setText(f'{value}°C')

        slider.valueChanged.connect(update_slider_label)

        slider_layout.addWidget(slider_label)
        slider_layout.addWidget(slider)
        layout.addLayout(slider_layout)

        # Value display
        layout.addWidget(value_label)

        # Only Ok button
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        def accept():
            new_temp = slider.value()
            self.presets[preset]['temperature'] = new_temp
            btn_text = f"{new_temp}°C, {self.presets[preset]['drying_time']} min"
            self.preset_buttons[preset].setText(btn_text)
            self.save_presets()
            dialog.accept()
            print(f'Updated {preset} to {btn_text}')
        button_box.accepted.connect(accept)
        layout.addWidget(button_box)

        dialog.setLayout(layout)
        dialog.exec()
    def add_preset(self):
        name = self.new_preset_name.text().strip()
        temp = self.new_preset_temp.text().strip()
        if not name or not temp:
            QMessageBox.warning(self, 'Input Error', 'Please enter both a name and temperature.')
            return
        if name in self.presets:
            QMessageBox.warning(self, 'Duplicate', 'Preset already exists.')
            return
        try:
            temp_val = int(temp.replace('°C', ''))
        except ValueError:
            QMessageBox.warning(self, 'Input Error', 'Temperature must be a number.')
            return
        self.presets[name] = {'temperature': temp_val, 'drying_time': 60}
        label = QLabel(f'{name}:')
        label.setFont(QFont('Arial', 14))
        btn_text = f"{temp_val}°C, 60 min"
        button = QPushButton(btn_text)
        button.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        button.setFixedSize(150, 60)
        import functools
        button.clicked.connect(functools.partial(self.open_slider_popup, name))
        self.preset_labels[name] = label
        self.preset_buttons[name] = button
        row = self.grid_layout.rowCount()
        self.grid_layout.addWidget(label, row, 0)
        self.grid_layout.addWidget(button, row, 1)
        self.save_presets()
        self.new_preset_name.clear()
        self.new_preset_temp.clear()
        
    def set_preset_value_and_close(self, preset, dialog):
        new_value = f'{self.slider.value()}°C'
        self.presets[preset] = new_value
        dialog.accept()
        print(f'Updated {preset} to {new_value}')
        
    def save_presets(self):
        if not self.presets or not isinstance(self.presets, dict):
            QMessageBox.critical(self, 'Error', 'No presets to save or presets data is invalid.')
            print('Presets dict is empty or invalid:', self.presets)
            return
        # Validate all preset entries
        for k, v in self.presets.items():
            if not isinstance(v, dict) or 'temperature' not in v or 'drying_time' not in v:
                QMessageBox.critical(self, 'Error', f'Preset "{k}" is invalid and will not be saved.')
                print(f'Invalid preset data for {k}:', v)
                return
        try:
            with open(self.presets_file, 'w') as file:
                json.dump(self.presets, file)
            # Update all button labels to reflect saved values
            for preset, button in self.preset_buttons.items():
                if preset in self.presets:
                    data = self.presets[preset]
                    if isinstance(data, dict):
                        btn_text = f"{data.get('temperature', '')}°C, {data.get('drying_time', '')} min"
                    else:
                        btn_text = str(data)
                    button.setText(btn_text)
            QMessageBox.information(self, 'Success', 'Presets saved successfully!')
            print('Presets saved:', self.presets)
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to save presets: {str(e)}')
            print(f'Failed to save presets: {e}')
