import os
import numpy as np
from pathlib import Path
from PySide6.QtWidgets import QWidget, QFrame, QPushButton
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from oscillator import SineOscillator as sine, SquareOscillator as square, TriangleOscillator as triangle, SawtoothOscillator as saw
from volume import Volume
import sounddevice as sd



SAMPLE_RATE = 48000
MAX_AMPLITUDE = 8192
DURATION = .2
DEFAULT_VOLUME = 9
DEFAULT_VOLUME_OFFSET = 9

# Define note frequencies
NOTE_FREQS = {
    # 2nd Octave
    "E2": 82.41,   # E2
    "F2": 87.31,   # F2
    "F#2": 92.50,  # F#2/Gb2
    "G2": 98.00,   # G2
    "G#2": 103.83, # G#2/Ab2
    "A2": 110.00,  # A2
    "A#2": 116.54, # A#2/Bb2
    "B2": 123.47,  # B2
    "C3": 130.81,  # C3
    "C#3": 138.59, # C#3/Db3
    "D3": 146.83,  # D3
    "D#3": 155.56, # D#3/Eb3

    # 3rd Octave
    "E3": 164.81,   # E3
    "F3": 174.61,   # F3
    "F#3": 185.00,  # F#3/Gb3
    "G3": 196.00,   # G3
    "G#3": 207.65,  # G#3/Ab3
    "A3": 220.00,   # A3
    "A#3": 233.08,  # A#3/Bb3
    "B3": 246.94,   # B3
    "C4": 261.63,   # C4
    "C#4": 277.18,  # C#4/Db4
    "D4": 293.66,   # D4
    "D#4": 311.13,  # D#4/Eb4

    # 4th Octave
    "E4": 329.63,   # E4
    "F4": 349.23,   # F4
    "F#4": 369.99,  # F#4/Gb4
    "G4": 392.00,   # G4
    "G#4": 415.30,  # G#4/Ab4
    "A4": 440.00,   # A4
    "A#4": 466.16,  # A#4/Bb4
    "B4": 493.88,   # B4
    "C5": 523.25,   # C5
    "C#5": 554.37,  # C#5/Db5
    "D5": 587.33,   # D5
    "D#5": 622.25,  # D#5/Eb5

    # 5th Octave
    "E5": 659.26,   # E5
    "F5": 698.46,   # F5
    "F#5": 739.99,  # F#5/Gb5
    "G5": 783.99,   # G5
    "G#5": 830.61,  # G#5/Ab5
    "A5": 880.00,   # A5
    "A#5": 932.33,  # A#5/Bb5
    "B5": 987.77,   # B5
    # Octave 6
    "C6": 1046.50   # C6
}

#generate a oscillator for each key inside a dictionary
#{"A4" : SineOscillator
# ...
# }
#Note: due to saw wave and square wave implementation, generating them takes a lot longer, might need rework in the future.
gained_waves = {}

sineWaves = {}
for key in NOTE_FREQS:
    oscillator = sine(NOTE_FREQS[key], SAMPLE_RATE, MAX_AMPLITUDE, DURATION)
    sineWaves[key] = oscillator.generateWave()

squareWaves = {}
for key in NOTE_FREQS:
    oscillator = square(NOTE_FREQS[key], SAMPLE_RATE, MAX_AMPLITUDE, DURATION)
    squareWaves[key] = oscillator.generateWave()

sawWaves = {}
for key in NOTE_FREQS:
    oscillator = square(NOTE_FREQS[key], SAMPLE_RATE, MAX_AMPLITUDE, DURATION)
    sawWaves[key] = oscillator.generateWave()

triangleWaves = {}
for key in NOTE_FREQS:
    oscillator = square(NOTE_FREQS[key], SAMPLE_RATE, MAX_AMPLITUDE, DURATION)
    triangleWaves[key] = oscillator.generateWave()

for key in NOTE_FREQS:
            gained_waves[key] = sineWaves[key].astype(np.int16)


class MainWidget(QWidget):  ### defines a class named MainWidget that inherits from QWidget class. The __init__() method initializes the object of the MainWidget class. The super() function is used to call the constructor of the parent class (QWidget) and to get the instance of the MainWidget class. This allows MainWidget to inherit all the attributes and methods from QWidget.
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


        #KEYBOARD KEYS
        #Find all keys in the GUI and assign event handlers to each
        keys = self.findChildren(QPushButton)
        for key in keys:
            note = key.objectName()
            key.pressed.connect(lambda note=note: self.button_pressed_handler(note))
            key.released.connect(self.button_released_handler)

        #VOLUME KNOB
        #Set up min, max, and default value of the volume knob
        win.volume_knob.setMinimum(0)
        win.volume_knob.setMaximum(10)
        win.volume_knob.setValue(DEFAULT_VOLUME)
        win.volume_knob.valueChanged.connect(self.handle_volume_changed)

        return win

    
    # Define a method for handling button releases
    def button_pressed_handler(self, key):   
        #Play the samples corresponding to a key
        sd.play(gained_waves[key], loop=True) 

    def button_released_handler(self):
        sd.stop() 
    

    #Whenever the knob is turned, get the new gain coefficient then apply to all keys
    def handle_volume_changed(self):
        knob_value = MainWidget.win.volume_knob.value()
        self.vol_ctrl.config(knob_value)
        for key in NOTE_FREQS:
            gained_waves[key] = self.vol_ctrl.change_gain(sineWaves[key]).astype(np.int16)


 