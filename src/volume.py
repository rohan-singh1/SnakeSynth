#This class handles volume processing for the GUI in form.py
#It contains a default value, and current value, from which the gain coefficient
#can be computed.
#The change_gain method will take a signal and returned an amplified version.

'''
The provided code defines a Volume class that handles volume processing for a GUI in the form.py module. 
The Volume class allows for changing the volume level and applying gain coefficients to audio signals. 
This class is designed to amplify or attenuate the volume of a given sound wave.

Usage
To use the Volume class in your project, follow these steps:

1. Import the Volume class from the appropriate module.
2. Create an instance of the Volume class, optionally specifying custom parameters for the initial 
setting and offset values.
3. Call the config() method to configure the volume setting based on a knob value or any other input.
4. The calculate_gain() method calculates the gain coefficient based on the current setting and offset values.
5. To change the gain of a sound wave, call the change_gain() method and pass the sound wave as a parameter. 
The method will return an amplified version of the sound wave.
'''
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

