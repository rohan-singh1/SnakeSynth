
# Copyright (c) 2018 Bart Massey
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.


'''Design inspired by 
https://python.plainenglish.io/build-your-own-python-synthesizer-part-2-66396f6dad81

The ADSREnvelope class represents an Attack-Decay-Sustain-Release (ADSR) envelope used in 
a synthesizer. This envelope is responsible for modulating the amplitude of the synthesized 
waveform over time, creating dynamic changes in the sound.

The Tone class represents the filter control typically found in synthesizers. This class contains 3 filters for
low end, mid range, and treble. The knob values control how loud each respective filter is compared to the others. Users can use a combination of knob configuration to alter the sound of a given sound.

To use the Tone class, follow these steps:

1. Create an instance of the Tone class and specify the knob value of each filter, the first frequency the the bass and mid filter, the second frequency for the mid and treble filter.
2. Call the 3 setters (set_bass, set_mid, set_treble) to update the knob_value and apply the filter.
3. Call filter with an np array of samples, which gives back a filtered sound wave with all three filters
'''

from scipy import io, signal
import numpy as np
import sounddevice as sd

DEFAULT_GAIN = 1.0
DEFAULT_KNOB_VAL = 5

class Tone():
    def __init__(self, bass_knob=DEFAULT_KNOB_VAL, mid_knob=DEFAULT_KNOB_VAL, treble_knob=DEFAULT_KNOB_VAL, first_stop=200, second_stop=2000, rate=48000):
        self._first_stop = first_stop
        self._second_stop = second_stop
        self._rate = rate

        self._bass_knob = bass_knob
        self._mid_knob = mid_knob
        self._treble_knob = treble_knob

        self._bass_filter = Filter('lowpass', rate, bass_knob, [first_stop] )
        self._mid_filter = Filter('bandpass', rate, mid_knob, [first_stop, second_stop])
        self._treble_filter = Filter('highpass', rate, mid_knob, [second_stop])

    def set_bass(self, knob_value):
        self._bass_filter.config(knob_value)

    def set_mid(self, knob_value):
        self._mid_filter.config(knob_value)

    def set_treble(self, knob_value):
        self._treble_filter.confg(knob_value)

    def filter(self, samples):
        low_passed = self._bass_filter.filter(samples)
        band_passed = self._mid_filter.filter(samples)
        high_passed = self._treble_filter.filter(samples)

        return low_passed + band_passed + high_passed


class Filter():
    def __init__(
        self,
        type='lowpass',
        rate=48000,
        knob_value=DEFAULT_KNOB_VAL,
        splits = [200]
    ):
        self._type = type
        self._rate: float = rate
        self._knob_value = knob_value
        self._splits = splits
        self._gain = DEFAULT_GAIN
        self.generate_coeff()

    # Build filters.
    def generate_coeff(self):
        freqs = 2.0 * np.array(self._splits, dtype=np.float64) / self._rate
        self._coeff = signal.firwin(255, freqs, pass_zero=self._type)
    
    #Filter sound wave
    def filter(self, samples):
        return signal.lfilter(self._coeff, self._splits,  samples) * self._gain


    #set gain
    def config(self, knob_value):
        self._knob_value = knob_value
        self._gain = self.tone_gain_converter(knob_value)

    # Convert from knob value to gain value for tone
    def tone_gain_converter(self, knob_value):
        if knob_value < 0.1:
            return 0
        db = 3.0 * (knob_value - 5)
        return pow(10.0, db / 20.0)

