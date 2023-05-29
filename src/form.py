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
from adsr import ADSREnvelope
from notefreq import NOTE_FREQS
from volume import Volume
import sounddevice as sd
import numpy as np

SAMPLE_RATE = 48000
MAX_AMPLITUDE = 8192
DURATION = 0.2
DEFAULT_VOLUME = 9
DEFAULT_VOLUME_OFFSET = 9
DEFAULT_ATTACK = 1
DEFAULT_DECAY = 2
DEFAULT_SUSTAIN = 8
DEFAULT_RELEASE = 5

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

selected = sine_waves

class MainWidget(
    QWidget
):  ### defines a class named MainWidget that inherits from QWidget class. The __init__() method initializes the object of the MainWidget class. The super() function is used to call the constructor of the parent class (QWidget) and to get the instance of the MainWidget class. This allows MainWidget to inherit all the attributes and methods from QWidget.
    def __init__(self):
        super(MainWidget, self).__init__()
        self.vol_ctrl = Volume(DEFAULT_VOLUME, DEFAULT_VOLUME_OFFSET)
        self.adsr_envelope = ADSREnvelope()
        MainWidget.win = self.load_ui()

    def load_ui(self):
        loader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parent / "../ui/form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        win = loader.load(ui_file, self)
        ui_file.close()
        self.set_default_values(win)

       

        # Connecting knob values to its corresponding spin box values
        win.attack_knob.valueChanged.connect(self.handle_attack_changed)
        win.decay_knob.valueChanged.connect(self.handle_decay_changed)
        win.sustain_knob.valueChanged.connect(self.handle_sustain_changed)
        win.release_knob.valueChanged.connect(self.handle_release_changed)
        win.pitch_knob.valueChanged.connect(self.handle_pitch_changed)
        win.tone_knob.valueChanged.connect(self.handle_tone_changed)
        win.volume_knob.valueChanged.connect(self.handle_volume_changed)

        # Connecting spin box values to its corresponding knob values
        win.attack_double_spin_box.valueChanged.connect(
            self.handle_attack_spin_box_value_changed
        )
        win.decay_double_spin_box.valueChanged.connect(
            self.handle_decay_spin_box_value_changed
        )
        win.sustain_double_spin_box.valueChanged.connect(
            self.handle_sustain_spin_box_value_changed
        )
        win.release_double_spin_box.valueChanged.connect(
            self.handle_release_spin_box_value_changed
        )
        win.pitch_double_spin_box.valueChanged.connect(
            self.handle_pitch_spin_box_value_changed
        )
        win.tone_double_spin_box.valueChanged.connect(
            self.handle_tone_spin_box_value_changed
        )
        win.volume_double_spin_box.valueChanged.connect(
            self.handle_volume_spin_box_value_changed
        )

        # Wave selection mechanism
        win.sine.clicked.connect(
            lambda: self.handle_waveform_selected("sine")
        )
        win.square.clicked.connect(
            lambda: self.handle_waveform_selected("square")
            )
        win.sawtooth.clicked.connect(
            lambda: self.handle_waveform_selected("sawtooth")
        )
        win.triangle.clicked.connect(
            lambda: self.handle_waveform_selected("triangle")
        )

        # KEYBOARD KEYS
        # Find all keys in the GUI and assign event handlers to each
        keys = win.keys_frame.findChildren(QPushButton)
        for key in keys:
            note = key.objectName()
            key.pressed.connect(lambda note=note: self.button_pressed_handler(note))
            key.released.connect(self.button_released_handler)

        # VOLUME KNOB
        # Set up default value of the volume knob
        win.volume_knob.setValue(DEFAULT_VOLUME)

        return win

    # Define a method for handling button releases
    def button_pressed_handler(self, key):
        #create envelope
        envelope = self.adsr_envelope.create_envelope(gained_waves[key])
        # Play the samples corresponding to a key
        sd.play(gained_waves[key], loop=True)

    def button_released_handler(self):
        sd.stop()

    def set_default_values(self, win):
        #default attack, sustain, release, decay values
        win.attack_knob.setValue(DEFAULT_ATTACK)
        win.attack_double_spin_box.setValue(DEFAULT_ATTACK)
        win.decay_knob.setValue(DEFAULT_DECAY)
        win.decay_double_spin_box.setValue(DEFAULT_DECAY)
        win.sustain_knob.setValue(DEFAULT_SUSTAIN)
        win.sustain_double_spin_box.setValue(DEFAULT_SUSTAIN)
        win.release_knob.setValue(DEFAULT_RELEASE)
        win.release_double_spin_box.setValue(DEFAULT_RELEASE)

        # Default wave selection
        win.sine.setChecked(True)
        self.handle_waveform_selected("sine")
    
    # Handle different wave types
    def handle_waveform_selected(self, selected_waveform):
        global selected_waves
        # Update the gained_waves dictionary based on the selected waveform
        if selected_waveform == "sine":
            selected_waves = sine_waves
            for key in NOTE_FREQS:
                gained_waves[key] = self.vol_ctrl.change_gain((sine_waves[key]))
        elif selected_waveform == "square":
            selected_waves = square_waves
            for key in NOTE_FREQS:
                gained_waves[key] = self.vol_ctrl.change_gain((square_waves[key]))
        elif selected_waveform == "sawtooth":
            selected_waves = saw_waves
            for key in NOTE_FREQS:
                gained_waves[key] = self.vol_ctrl.change_gain((saw_waves[key]))
        elif selected_waveform == "triangle":
            selected_waves = triangle_waves
            for key in NOTE_FREQS:
                gained_waves[key] = self.vol_ctrl.change_gain((triangle_waves[key]))
        else:
            QMessageBox.warning(self, "Invalid Waveform", "Invalid waveform selected!")

        

    #
    # Handle knob values changed
    #

    def handle_attack_changed(self, value):
        # Reflect the Attack spin box value as per the current value of the Attack dial
        self.win.attack_double_spin_box.setValue(self.win.attack_knob.value())
        self.adsr_envelope.update_attack(value)
        print("attack changed")

    def handle_decay_changed(self, value):
        # Reflect the Decay spin box value as per the current value of the Decay dial
        self.win.decay_double_spin_box.setValue(self.win.decay_knob.value())
        self.adsr_envelope.update_decay(value)
        print("decay changed")

    def handle_sustain_changed(self, value):
        # Reflect the Sustain spin box value as per the current value of the Sustain dial
        self.win.sustain_double_spin_box.setValue(self.win.sustain_knob.value())
        self.adsr_envelope.update_sustain(value)
        print("sustain changed")

    def handle_release_changed(self, value):
        # Reflect the Release spin box value as per the current value of the Release dial
        self.win.release_double_spin_box.setValue(self.win.release_knob.value())
        self.adsr_envelope.update_release(value)
        print("release changed")

    def handle_pitch_changed(self):
        # Reflect the Pitch spin box value as per the current value of the Pitch dial
        self.win.pitch_double_spin_box.setValue(self.win.pitch_knob.value())

    def handle_tone_changed(self):
        # Reflect the Tone spin box value as per the current value of the Tone dial
        self.win.tone_double_spin_box.setValue(self.win.tone_knob.value())

    # Whenever the knob is turned, get the new gain coefficient then apply to all keys
    def handle_volume_changed(self):
        knob_value = self.win.volume_knob.value()
        self.win.volume_double_spin_box.setValue(knob_value)
        print(knob_value)
        self.vol_ctrl.config(knob_value)
        for key in NOTE_FREQS:
            gained_waves[key] = self.vol_ctrl.change_gain(selected_waves[key]).astype(np.int16)

    #
    # Handle spin box values changed
    #

    def handle_attack_spin_box_value_changed(self):
        # Reflect the Attack dial value as per the current value of the Attack spin box
        self.win.attack_knob.setValue(self.win.attack_double_spin_box.value())

    def handle_decay_spin_box_value_changed(self):
        # Reflect the Decay dial value as per the current value of the Decay spin box
        self.win.decay_knob.setValue(self.win.decay_double_spin_box.value())

    def handle_sustain_spin_box_value_changed(self):
        # Reflect the Sustain dial value as per the current value of the Sustain spin box
        self.win.sustain_knob.setValue(self.win.sustain_double_spin_box.value())

    def handle_release_spin_box_value_changed(self):
        # Reflect the Release dial value as per the current value of the Release spin box
        self.win.release_knob.setValue(self.win.release_double_spin_box.value())

    def handle_pitch_spin_box_value_changed(self):
        # Reflect the Pitch dial value as per the current value of the Pitch spin box
        self.win.pitch_knob.setValue(self.win.pitch_double_spin_box.value())

    def handle_tone_spin_box_value_changed(self):
        # Reflect the Tone dial value as per the current value of the Tone spin box
        self.win.tone_knob.setValue(self.win.tone_double_spin_box.value())

    def handle_volume_spin_box_value_changed(self):
        # Reflect the Volume dial value as per the current value of the Volume spin box
        self.win.volume_knob.setValue(self.win.volume_double_spin_box.value())
