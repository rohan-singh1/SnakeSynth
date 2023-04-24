from abc import ABC
import numpy as np
import sounddevice as sd

class Oscillator(ABC):
    def __init__(self, frequency=440.0, sampleRate=48000, amplitude=np.iinfo(np.int16).max//4, duration=1.0):
        self._fundamentalFrequency = 440.0
        self._frequency: float = frequency
        self._sampleRate: int = sampleRate
        self._amplitude: float = amplitude
        self._duration: float = duration
        self._stepSize: float = 1.0 / sampleRate
        self._time = np.arange(0, self._duration, self._stepSize)
        self._pitchCoefficient = self._frequency / self._fundamentalFrequency

    def generateWave(self):
        pass

class SineOscillator(Oscillator):
    def __init__(self, frequency=440, sampleRate=48000, amplitude=np.iinfo(np.int16).max//4, duration=1.0):
        super().__init__(frequency=frequency, sampleRate=sampleRate, amplitude=amplitude, duration=duration)
    
    def generateWave(self):
        return self._amplitude * np.sin(self._pitchCoefficient * np.pi * self._frequency * self._time)

if __name__ == "__main__":
    sine = SineOscillator()
    wave = sine.generateWave()
    sd.play(wave, sine._sampleRate)
    sd.wait()