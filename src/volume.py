#This class handles volume processing for the GUI in form.py
#It contains a default value, and current value, from which the gain coefficient
#can be computed.
#The change_gain method will take a signal and returned an amplified version.

import numpy as np

class Volume():
    def __init__(self, setting=9, offset=9):
        self._setting = setting
        self._offset = offset
        self._gain = self.calculate_gain()

    #configurate all volume parameter given a knob value
    def config(self,setting):
        self._setting = setting
        self._gain = self.calculate_gain()

    #calculate the gain coefficient based on default offset and current knob setting
    def calculate_gain(self):
        if self._setting < 0.1:
            return 0
        db = 3.0 * (self._setting - self._offset)
        return pow(10.0 , db / 20.0)
    
    #change the gain of a given sound wave
    def change_gain(self, samples):
        return (samples * self._gain).astype(np.int16)

