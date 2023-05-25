import os
from pathlib import Path
from PySide6.QtWidgets import QWidget, QFrame, QPushButton, QRadioButton, QMessageBox
from PySide6.QtCore import QFile, Qt
from PySide6.QtUiTools import QUiLoader
from oscillator import (
    SineOscillator as sine,
    SquareOscillator as square,
    TriangleOscillator as triangle,
    SawtoothOscillator as saw,
)
from notefreq import NOTE_FREQS
from volume import Volume
import sounddevice as sd
import numpy as np

SAMPLE_RATE = 48000
MAX_AMPLITUDE = 8192
DURATION = 0.2
DEFAULT_VOLUME = 9
DEFAULT_VOLUME_OFFSET = 9

# generate a oscillator for each key inside a dictionary
# {"A4" : SineOscillator
# ...
# }
# Note: due to saw wave and square wave implementation, generating them takes a lot longer, might need rework in the future.
gained_waves = {}

sine_waves = {}
for key in NOTE_FREQS:
    oscillator = sine(NOTE_FREQS[key], SAMPLE_RATE, MAX_AMPLITUDE, DURATION)
    sine_waves[key] = oscillator.generate_wave()

square_waves = {}
for key in NOTE_FREQS:
    oscillator = square(NOTE_FREQS[key], SAMPLE_RATE, MAX_AMPLITUDE, DURATION)
    square_waves[key] = oscillator.generate_wave()

saw_waves = {}
for key in NOTE_FREQS:
    oscillator = saw(NOTE_FREQS[key], SAMPLE_RATE, MAX_AMPLITUDE, DURATION)
    saw_waves[key] = oscillator.generate_wave()

triangle_waves = {}
for key in NOTE_FREQS:
    oscillator = triangle(NOTE_FREQS[key], SAMPLE_RATE, MAX_AMPLITUDE, DURATION)
    triangle_waves[key] = oscillator.generate_wave()


class MainWidget(
    QWidget
):  ### defines a class named MainWidget that inherits from QWidget class. The __init__() method initializes the object of the MainWidget class. The super() function is used to call the constructor of the parent class (QWidget) and to get the instance of the MainWidget class. This allows MainWidget to inherit all the attributes and methods from QWidget.
    def __init__(self):
        super(MainWidget, self).__init__()
        MainWidget.win = self.load_ui()
        self.vol_ctrl = Volume(DEFAULT_VOLUME, DEFAULT_VOLUME_OFFSET)

    def load_ui(self):
        loader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parent / "../ui/form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        win = loader.load(ui_file, self)
        ui_file.close()

        #variables to hold the radio selections
        sine_radio = win.sin
        square_radio = win.square
        sawtooth_radio = win.sawtooth
        triangle_radio = win.triangle

        #default wave selection
        sine_radio.setChecked(True)
        self.handle_waveform_selected("sine")

        #Wave selection mechanism
        sine_radio.clicked.connect(lambda: self.handle_waveform_selected("sine"))
        square_radio.clicked.connect(lambda: self.handle_waveform_selected("square"))
        sawtooth_radio.clicked.connect(lambda: self.handle_waveform_selected("sawtooth"))
        triangle_radio.clicked.connect(lambda: self.handle_waveform_selected("triangle"))
        

        # KEYBOARD KEYS
        # Find all keys in the GUI and assign event handlers to each
        keys = self.findChildren(QPushButton)
        for key in keys:
            note = key.objectName()
            key.pressed.connect(lambda note=note: self.button_pressed_handler(note))
            key.released.connect(self.button_released_handler)

        # VOLUME KNOB
        # Set up default value of the volume knob
        win.volume_knob.setValue(DEFAULT_VOLUME)
        win.volume_knob.valueChanged.connect(self.handle_volume_changed)

        return win

    # Define a method for handling button releases
    def button_pressed_handler(self, key):
        # Play the samples corresponding to a key
        sd.play(gained_waves[key], loop=True)

    def button_released_handler(self):
        sd.stop()

    # Whenever the knob is turned, get the new gain coefficient then apply to all keys
    def handle_volume_changed(self):
        knob_value = MainWidget.win.volume_knob.value()
        self.vol_ctrl.config(knob_value)
        for key in NOTE_FREQS:
            gained_waves[key] = self.vol_ctrl.change_gain(gained_waves[key]).astype(np.int16)
    #handle different wave types
    def handle_waveform_selected(self, selected_waveform):

        # Update the gained_waves dictionary based on the selected waveform
        if selected_waveform == "sine":
            for key in NOTE_FREQS:
                gained_waves[key] = sine_waves[key].astype(np.int16)
        elif selected_waveform == "square":
            for key in NOTE_FREQS:
                gained_waves[key] = square_waves[key].astype(np.int16)
        elif selected_waveform == "sawtooth":
            for key in NOTE_FREQS:
                gained_waves[key] = saw_waves[key].astype(np.int16)
        elif selected_waveform == "triangle":
            for key in NOTE_FREQS:
                gained_waves[key] = triangle_waves[key].astype(np.int16)
        else:
            QMessageBox.warning(self, "Invalid Waveform", "Invalid waveform selected!")