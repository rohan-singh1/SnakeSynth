import os
from pathlib import Path
from PySide6.QtWidgets import QWidget, QFrame, QPushButton
from PySide6.QtCore import QFile
from PySide6.QtCore import Qt
from PySide6.QtUiTools import QUiLoader
from oscillator import SineOscillator as sine, SquareOscillator as square, TriangleOscillator as triangle, SawtoothOscillator as saw
from notefreq import NOTE_FREQS


SAMPLE_RATE = 48000
AMPLITUDE = 8192
DURATION = 1.0


#generate a oscillator for each key inside a dictionary
#{"A4" : SineOscillator
# ...
# }
#Note: due to saw wave and square wave implementation, generating them takes a lot longer, might need rework in the future.
sineWaves = {}
for key in NOTE_FREQS:
    sineWaves[key] = sine(NOTE_FREQS[key],SAMPLE_RATE, AMPLITUDE, DURATION)

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
        win.snake_synth_label.setAttribute(Qt.WA_TransparentForMouseEvents) # So the label doesn't consume mouse events
        ui_file.close()


        #Find all keys in the GUI and assign event handlers to each
        keys = self.findChildren(QPushButton)
        for key in keys:
            note = key.objectName()
            key.pressed.connect(lambda note=note: self.button_pressed_handler(note))
            key.released.connect(self.button_released_handler)

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
 