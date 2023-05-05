from abc import ABC
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plot
import pyaudio

class Oscillator(ABC):
    def __init__(self, frequency=220.0, sampleRate=48000, amplitude=np.iinfo(np.int16).max/4, duration=1.0):
        p = pyaudio.PyAudio()
        self._frequency: float = frequency
        self._sampleRate: int = sampleRate
        self._amplitude: float = amplitude
        self._duration: float = duration
        self._stepSize: float = 2.0 * np.pi * self._frequency / sampleRate
        #self._time = np.arange(p.get_sample_size(format=pyaudio.paInt16) * self._sampleRate * self._duration)
        self._time = np.arange(self._sampleRate * self._duration)


    def generateWave(self):
        pass


#SINE OSCILLATOR
class SineOscillator(Oscillator):
    def __init__(self, frequency=440, sampleRate=48000, amplitude=np.iinfo(np.int16).max/4, duration=1.0):
        super().__init__(frequency=frequency, sampleRate=sampleRate, amplitude=amplitude, duration=duration)
    
    def generateWave(self):
        return self._amplitude * np.sin(self._stepSize * self._time)

class SquareOscillator(SineOscillator):
    def __init__(self, frequency=440, sampleRate=48000, amplitude=np.iinfo(np.int16).max/4, duration=1.0):
        super().__init__(frequency=frequency, sampleRate=sampleRate, amplitude=amplitude, duration=duration)
    
    def generateWave(self):
        samples = np.sin(self._stepSize * self._time)
        for x in np.nditer(samples, op_flags=['readwrite']):
            if x[...] >= 0:
                x[...] = self._amplitude
            else:
                x[...] = -self._amplitude
        return samples


#TRIANGLE OSCILLATOR
#Source: https://stackoverflow.com/questions/1073606/is-there-a-one-line-function-that-generates-a-triangle-wave
class TriangleOscillator(Oscillator):
    def __init__(self, frequency=440, sampleRate=48000, amplitude=np.iinfo(np.int16).max/4, duration=1.0):
        super().__init__(frequency=frequency, sampleRate=sampleRate, amplitude=amplitude, duration=duration)
    
    def generateWave(self):
        samples = np.arange(self._sampleRate * self._duration)

        #half-period
        hp = (1 / self._frequency) / 2

        #double the amplitude
        da = self._amplitude * 2

        for x in np.nditer(samples, op_flags=['readwrite']):
            x[...] = da/hp * (hp - np.abs(np.mod(x/self._sampleRate + hp/2,(2*hp))-hp)) - self._amplitude
        return samples

#SAW TOOTH OSCILLATOR
class SawtoothOscillator(Oscillator):
    def __init__(self, frequency=440, sampleRate=48000, amplitude=np.iinfo(np.int16).max/4, duration=1.0):
        super().__init__(frequency=frequency, sampleRate=sampleRate, amplitude=amplitude, duration=duration)
    
    def generateWave(self):
        samples = np.arange(self._sampleRate * self._duration)
        for x in np.nditer(samples, op_flags=['readwrite']):
            x[...] = 2 * np.fmod(((x * 4 * self._amplitude)/ self._frequency)+self._amplitude/2, self._amplitude) - self._amplitude
        return samples


if __name__ == "__main__":
    frequency = 440
    sampleRate = 48000
    amplitude=np.iinfo(np.int16).max/4
    duration=1.0

    sine = SineOscillator(frequency, sampleRate, amplitude, duration)
    square = SquareOscillator(frequency, sampleRate, amplitude, duration)
    triangle = TriangleOscillator(frequency, sampleRate, amplitude, duration)
    sawtooth = SawtoothOscillator(frequency, sampleRate, amplitude, duration)

    wave = triangle.generateWave().astype(np.int16)

    plot.plot( sawtooth._time[:int(sampleRate/frequency)], wave[:int(sampleRate/frequency)])
    plot.show()
    
    sd.play(wave, triangle._sampleRate)
    sd.wait()