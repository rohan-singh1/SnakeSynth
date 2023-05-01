from abc import ABC
import numpy as np
import sounddevice as sd
import pyaudio

class Oscillator(ABC):
    def __init__(self, frequency=440.0, sampleRate=48000, amplitude=np.iinfo(np.int16).max//4, duration=1.0):
        p = pyaudio.PyAudio()
        self._frequency: float = frequency
        self._sampleRate: int = sampleRate
        self._amplitude: float = amplitude
        self._duration: float = duration
        self._stepSize: float = 2.0 * np.pi * self._frequency / sampleRate
        self._time = np.arange(p.get_sample_size(format=pyaudio.paFloat32) * self._sampleRate * self._duration)

    def generateWave(self):
        pass

class SineOscillator(Oscillator):
    def __init__(self, frequency=440, sampleRate=48000, amplitude=np.iinfo(np.int16).max//4, duration=1.0):
        super().__init__(frequency=frequency, sampleRate=sampleRate, amplitude=amplitude, duration=duration)
    
    def generateWave(self):
        return self._amplitude * np.sin(self._stepSize * self._time)

class SquareOscillator(SineOscillator):
    def __init__(self, frequency=440, sampleRate=48000, amplitude=np.iinfo(np.int16).max//4, duration=1.0):
        super().__init__(frequency=frequency, sampleRate=sampleRate, amplitude=amplitude, duration=duration)
    
    def generateWave(self):
        pass

class TriangleOscillator(Oscillator):
    def __init__(self, frequency=440, sampleRate=48000, amplitude=np.iinfo(np.int16).max//4, duration=1.0):
        super().__init__(frequency=frequency, sampleRate=sampleRate, amplitude=amplitude, duration=duration)
    
    def generateWave(self):
        pass
class SawtoothOscillator(Oscillator):
    def __init__(self, frequency=440, sampleRate=48000, amplitude=np.iinfo(np.int16).max//4, duration=1.0):
        super().__init__(frequency=frequency, sampleRate=sampleRate, amplitude=amplitude, duration=duration)
    
    def generateWave(self):
        pass

if __name__ == "__main__":
    sine = SineOscillator()
    wave = sine.generateWave()
    sd.play(wave, sine._sampleRate)
    sd.wait()