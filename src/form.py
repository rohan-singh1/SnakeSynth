import os
import sine_tone   # Import the required modules

from pathlib import Path   # Import the Path class from the pathlib module
from PySide6.QtWidgets import QWidget   # Import the QWidget class from the PySide6.QtWidgets module
from PySide6.QtCore import QFile   # Import the QFile class from the PySide6.QtCore module
from PySide6.QtUiTools import QUiLoader   # Import the QUiLoader class from the PySide6.QtUiTools module


dur = 3

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

class MainWidget(QWidget):  ### defines a class named MainWidget that inherits from QWidget class. The __init__() method initializes the object of the MainWidget class. The super() function is used to call the constructor of the parent class (QWidget) and to get the instance of the MainWidget class. This allows MainWidget to inherit all the attributes and methods from QWidget.
    def __init__(self):
        super(MainWidget, self).__init__()
        MainWidget.win = self.load_ui()   # Call the load_ui method to load the UI from an XML file

    def load_ui(self):
        loader = QUiLoader()   # Create a new QUiLoader object
        path = os.fspath(Path(__file__).resolve().parent / "../ui/form.ui")   # Get the path to the UI file
        ui_file = QFile(path)   # Create a new QFile object for the UI file
        ui_file.open(QFile.ReadOnly)   # Open the UI file in read-only mode
        win = loader.load(ui_file, self)   # Load the UI from the file using the QUiLoader object
        ui_file.close()   # Close the UI file

        # Connecting UI signals to their respective slots
        # White Keys 2-13 
        win.pushButton_2.pressed.connect(self.handle_button2_pressed)       # Connect the pressed signal of pushButton_2 to the handle_button_pressed method
        win.pushButton_2.released.connect(self.handle_button_released)
        win.pushButton_3.pressed.connect(self.handle_button3_pressed)
        win.pushButton_3.released.connect(self.handle_button_released)
        win.pushButton_4.pressed.connect(self.handle_button4_pressed)
        win.pushButton_4.released.connect(self.handle_button_released)
        win.pushButton_5.pressed.connect(self.handle_button5_pressed)
        win.pushButton_5.released.connect(self.handle_button_released)

        win.pushButton_6.pressed.connect(self.handle_button6_pressed)
        win.pushButton_6.released.connect(self.handle_button_released)
        win.pushButton_7.pressed.connect(self.handle_button7_pressed)
        win.pushButton_7.released.connect(self.handle_button_released)
        win.pushButton_8.pressed.connect(self.handle_button8_pressed)
        win.pushButton_8.released.connect(self.handle_button_released)



        win.pushButton_16.pressed.connect(self.handle_button16_pressed)
        win.pushButton_16.released.connect(self.handle_button_released)

        win.pushButton_9.pressed.connect(self.handle_button9_pressed)
        win.pushButton_9.released.connect(self.handle_button_released)
 
        win.pushButton_15.pressed.connect(self.handle_button15_pressed)
        win.pushButton_15.released.connect(self.handle_button_released)

        win.pushButton_14.pressed.connect(self.handle_button14_pressed)
        win.pushButton_14.released.connect(self.handle_button_released)

        win.pushButton_10.pressed.connect(self.handle_button10_pressed)
        win.pushButton_10.released.connect(self.handle_button_released)
        win.pushButton_11.pressed.connect(self.handle_button11_pressed)
        win.pushButton_11.released.connect(self.handle_button_released)
        win.pushButton_12.pressed.connect(self.handle_button12_pressed)
        win.pushButton_12.released.connect(self.handle_button_released)
        win.pushButton_13.pressed.connect(self.handle_button13_pressed)
        win.pushButton_13.released.connect(self.handle_button_released)

        # Black Keys 17-26
        win.pushButton_17.pressed.connect(self.handle_button17_pressed)      # Connect the pressed signal of pushButton_3 to the handle_button2_pressed method
        win.pushButton_17.released.connect(self.handle_button_released)     # Connect the released signal of pushButton_3 to the handle_button_released method
        win.pushButton_18.pressed.connect(self.handle_button18_pressed)      # Connect the pressed signal of pushButton_3 to the handle_button2_pressed method
        win.pushButton_18.released.connect(self.handle_button_released)     # Connect the released signal of pushButton_3 to the handle_button_released method
        win.pushButton_19.pressed.connect(self.handle_button19_pressed)      # Connect the pressed signal of pushButton_3 to the handle_button2_pressed method
        win.pushButton_19.released.connect(self.handle_button_released)     # Connect the released signal of pushButton_3 to the handle_button_released method
        win.pushButton_20.pressed.connect(self.handle_button20_pressed)      # Connect the pressed signal of pushButton_3 to the handle_button2_pressed method
        win.pushButton_20.released.connect(self.handle_button_released)     # Connect the released signal of pushButton_3 to the handle_button_released method
        win.pushButton_21.pressed.connect(self.handle_button21_pressed)      # Connect the pressed signal of pushButton_3 to the handle_button2_pressed method
        win.pushButton_21.released.connect(self.handle_button_released)     # Connect the released signal of pushButton_3 to the handle_button_released method
        win.pushButton_22.pressed.connect(self.handle_button22_pressed)      # Connect the pressed signal of pushButton_3 to the handle_button2_pressed method
        win.pushButton_22.released.connect(self.handle_button_released)     # Connect the released signal of pushButton_3 to the handle_button_released method
        win.pushButton_23.pressed.connect(self.handle_button23_pressed)      # Connect the pressed signal of pushButton_3 to the handle_button2_pressed method
        win.pushButton_23.released.connect(self.handle_button_released)     # Connect the released signal of pushButton_3 to the handle_button_released method
        win.pushButton_24.pressed.connect(self.handle_button24_pressed)      # Connect the pressed signal of pushButton_3 to the handle_button2_pressed method
        win.pushButton_24.released.connect(self.handle_button_released)     # Connect the released signal of pushButton_3 to the handle_button_released method
        win.pushButton_25.pressed.connect(self.handle_button25_pressed)      # Connect the pressed signal of pushButton_3 to the handle_button2_pressed method
        win.pushButton_25.released.connect(self.handle_button_released)     # Connect the released signal of pushButton_3 to the handle_button_released method
        win.pushButton_26.pressed.connect(self.handle_button26_pressed)      # Connect the pressed signal of pushButton_3 to the handle_button2_pressed method
        win.pushButton_26.released.connect(self.handle_button_released)     # Connect the released signal of pushButton_3 to the handle_button_released method

        # Volume Knob
        win.volume_knob.valueChanged.connect(self.handle_volume_changed)   # Connect the valueChanged signal of the volume_knob slider to the handle_volume_changed method

        return win   # Return the loaded UI

    def handle_volume_changed(value):   # Define a method for handling changes to the volume knob
        print("Current volume: ", MainWidget.win.volume_knob.value())   # Print the current volume value to the console

# White keys: 
    def handle_button2_pressed(toggled):   # Define a method for handling the press of a second button
        sine_tone.oscillator_sine(NOTE_FREQS["C3"],dur)   # Call the play_sine method from the sine_tone module to start playing a sine tone

    def handle_button3_pressed(toggled):   # Define a method for handling the press of a second button
        sine_tone.oscillator_sine(NOTE_FREQS["D3"],dur)   # Call the play_sine method from the sine_tone module to start playing a sine tone

    def handle_button4_pressed(toggled):   # Define a method for handling button presses
        sine_tone.oscillator_sine(NOTE_FREQS["E3"],dur)   # Call the play_sine method from the sine_tone module to start playing a sine tone

    def handle_button5_pressed(toggled):   # Define a method for handling the press of a second button
        sine_tone.oscillator_sine(NOTE_FREQS["F3"],dur)   # Call the play_sine method from the sine_tone module to start playing a sine tone

    def handle_button6_pressed(toggled):   # Define a method for handling the press of a second button
        sine_tone.oscillator_sine(NOTE_FREQS["G3"],dur)   # Call the play_sine method from the sine_tone module to start playing a sine tone

    def handle_button7_pressed(toggled):   # Define a method for handling the press of a second button
        sine_tone.oscillator_sine(NOTE_FREQS["A3"],dur)   # Call the play_sine method from the sine_tone module to start playing a sine tone


    def handle_button8_pressed(toggled):   # Define a method for handling the press of a second button
        sine_tone.oscillator_sine(NOTE_FREQS["B3"],dur)   # Call the play_sine method from the sine_tone module to start playing a sine tone


    def handle_button16_pressed(toggled):   # Define a method for handling the press of a second button
        sine_tone.oscillator_sine(NOTE_FREQS["C4"],dur)   # Call the play_sine method from the sine_tone module to start playing a sine tone

    def handle_button9_pressed(toggled):   # Define a method for handling the press of a second button
        sine_tone.oscillator_sine(NOTE_FREQS["D4"],dur)   # Call the play_sine method from the sine_tone module to start playing a sine tone

    def handle_button15_pressed(toggled):   # Define a method for handling the press of a second button
        sine_tone.oscillator_sine(NOTE_FREQS["E4"],dur)   # Call the play_sine method from the sine_tone module to start playing a sine tone

    def handle_button14_pressed(toggled):   # Define a method for handling the press of a second button
        sine_tone.oscillator_sine(NOTE_FREQS["F4"],dur)   # Call the play_sine method from the sine_tone module to start playing a sine tone

    def handle_button10_pressed(toggled):   # Define a method for handling the press of a second button
        sine_tone.oscillator_sine(NOTE_FREQS["G4"],dur)   # Call the play_sine method from the sine_tone module to start playing a sine tone

    def handle_button11_pressed(toggled):   # Define a method for handling the press of a second button
        sine_tone.oscillator_sine(NOTE_FREQS["A4"],dur)   # Call the play_sine method from the sine_tone module to start playing a sine tone

    def handle_button12_pressed(toggled):   # Define a method for handling the press of a second button
        sine_tone.oscillator_sine(NOTE_FREQS["B4"],dur)   # Call the play_sine method from the sine_tone module to start playing a sine tone

    def handle_button13_pressed(toggled):   # Define a method for handling the press of a second button
        sine_tone.oscillator_sine(NOTE_FREQS["C5"],dur)   # Call the play_sine method from the sine_tone module to start playing a sine tone

#Black Keys: 
    def handle_button17_pressed(toggled):   # Define a method for handling button presses
        sine_tone.oscillator_sine(NOTE_FREQS["C#3"],dur)   # Call the play_sine method from the sine_tone module to start playing a sine tone
   

    def handle_button18_pressed(toggled):   # Define a method for handling the press of a second button
        sine_tone.oscillator_sine(NOTE_FREQS["D#3"],dur)   # Call the play_sine method from the sine_tone module to start playing a sine tone


    def handle_button19_pressed(toggled):   # Define a method for handling the press of a second button
        sine_tone.oscillator_sine(NOTE_FREQS["F#3"],dur)   # Call the play_sine method from the sine_tone module to start playing a sine tone



    def handle_button20_pressed(toggled):   # Define a method for handling the press of a second button
        sine_tone.oscillator_sine(NOTE_FREQS["G#3"],dur)   # Call the play_sine method from the sine_tone module to start playing a sine tone



    def handle_button21_pressed(toggled):   # Define a method for handling the press of a second button
        sine_tone.oscillator_sine(NOTE_FREQS["A#3"],dur)   # Call the play_sine method from the sine_tone module to start playing a sine tone




    def handle_button22_pressed(toggled):   # Define a method for handling the press of a second button
        sine_tone.oscillator_sine(NOTE_FREQS["C#4"],dur)   # Call the play_sine method from the sine_tone module to start playing a sine tone


    def handle_button23_pressed(toggled):   # Define a method for handling the press of a second button
        sine_tone.oscillator_sine(NOTE_FREQS["D#4"],dur)   # Call the play_sine method from the sine_tone module to start playing a sine tone


    def handle_button24_pressed(toggled):   # Define a method for handling the press of a second button
        sine_tone.oscillator_sine(NOTE_FREQS["F#4"],dur)   # Call the play_sine method from the sine_tone module to start playing a sine tone

    def handle_button25_pressed(toggled):   # Define a method for handling the press of a second button
        sine_tone.oscillator_sine(NOTE_FREQS["G#4"],dur)   # Call the play_sine method from the sine_tone module to start playing a sine tone

    def handle_button26_pressed(toggled):   # Define a method for handling the press of a second button
        sine_tone.oscillator_sine(NOTE_FREQS["A#4"],dur)   # Call the play_sine method from the sine_tone module to start playing a sine tone



    def handle_button_released(toggled):   # Define a method for handling button releases
        sine_tone.stop_playing()   # Call the stop_playing method from the sine_tone module to stop playing the sine tone