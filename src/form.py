import os
import sine_tone

from pathlib import Path
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader


class MainWidget(QWidget):
    def __init__(self):
        super(MainWidget, self).__init__()
        MainWidget.win = self.load_ui()

    def load_ui(self):
        loader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parent / "../ui/form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        win = loader.load(ui_file, self)
        ui_file.close()

        # Connecting UI signals to their respective slots
        win.pushButton_2.pressed.connect(self.handle_button_pressed)
        win.pushButton_2.released.connect(self.handle_button_released)
        win.pushButton_3.pressed.connect(self.handle_button2_pressed)
        win.pushButton_3.released.connect(self.handle_button_released)
        win.volume_knob.valueChanged.connect(self.handle_volume_changed)

        return win

    def handle_volume_changed(value):
        print("Current volume: ", MainWidget.win.volume_knob.value())

    def handle_button_pressed(toggled):
        sine_tone.play_sine(2)
        
    def handle_button_released(toggled):
        sine_tone.stop_playing()

    def handle_button2_pressed(toggled):
        sine_tone.play_sine(2.2)

        