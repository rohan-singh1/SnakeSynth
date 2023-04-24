from abc import ABC, abstractmethod
import numpy as np

class Oscillator(ABC):
    def __init__(self, frequency=440, sampleRate=48000, amplitude=1.0, duration=1.0):
        self._frequency = frequency
        self._sampleRate = sampleRate
        self._amplitude = amplitude
        self._duration = duration
        self._stepSize = 1.0 / sampleRate
        self._time = np.arange(0, self._duration, self._stepSize)

    def generateWave(self):
        pass

class SineOscillator(Oscillator):
    def __init__(self, frequency=440, sampleRate=48000, amplitude=1.0, duration=1.0):
        super().__init__(frequency=frequency, sampleRate=sampleRate, amplitude=amplitude, duration=duration)
    
    def generateWave(self):
        return self._amplitude * np.sin(2. * np.pi * self._frequency * self._time)