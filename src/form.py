import os
import sine_tone

from pathlib import Path
from PySide6.QtWidgets import QWidget, QFrame, QPushButton
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from oscillator import SineOscillator as sine, SquareOscillator as square, TriangleOscillator as triangle, SawtoothOscillator as saw



dur = 5
sampleRate = 48000
amplitude = 8912
duration = 1.0

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
sineWaves = {}
for key in NOTE_FREQS:
    sineWaves[key] = saw(NOTE_FREQS[key],sampleRate, amplitude, duration)

class MainWidget(QWidget):  ### defines a class named MainWidget that inherits from QWidget class. The __init__() method initializes the object of the MainWidget class. The super() function is used to call the constructor of the parent class (QWidget) and to get the instance of the MainWidget class. This allows MainWidget to inherit all the attributes and methods from QWidget.
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


        #Find all keys in the GUI and assign event handlers to each
        keys = self.findChildren(QPushButton)
        for key in keys:
            note = key.objectName()
            key.pressed.connect(lambda note=note: self.button_pressed_handler(note))
            key.released.connect(lambda: self.button_released_handler)

        win.volume_knob.valueChanged.connect(self.handle_volume_changed)

        return win
    
    # Define a method for handling button releases
    def button_pressed_handler(self, key):   
        #Play the oscillator corresponding to a key
        sineWaves[key].play()  

    def button_released_handler(self):
        #Stop the oscillator
        sineWaves[key].stop()  
    
    def handle_volume_changed(value):
        print("Current volume: ", MainWidget.win.volume_knob.value())
 