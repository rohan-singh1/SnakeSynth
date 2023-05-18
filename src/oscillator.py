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
        self._time = np.arange(int(self._sampleRate * self._duration))
        self._samples = np.array(0)
        self._gainedSamples = np.array(0)

    def generateWave(self):
        pass

    def play(self):
        sd.play(self._gainedSamples.astype(np.int16), self._sampleRate)
        print(self._samples[-1])

    #Crop the samples to the final zero crossing, so that the end of a wave match up with the beginning
    #Side effects: final signal is very slightly shorter.
    def crop_samples(self, samples):
        samplesPerPeriod = (self._sampleRate / self._frequency)
        remainder = round(self._time.size % samplesPerPeriod)

        return samples[0:self._time.size - remainder]

    
    def stop(self):
        sd.stop()



#SINE OSCILLATOR
class SineOscillator(Oscillator):
    def __init__(self, frequency=440, sampleRate=48000, amplitude=np.iinfo(np.int16).max/4, duration=1.0):
        super().__init__(frequency=frequency, sampleRate=sampleRate, amplitude=amplitude, duration=duration)
        self._samples = self.generateWave()
        self._gainedSamples = self._samples
    
    def generateWave(self):
        samples = self._amplitude * np.sin(self._stepSize * self._time)

        return self.crop_samples(samples)


class SquareOscillator(SineOscillator):
    def __init__(self, frequency=440, sampleRate=48000, amplitude=np.iinfo(np.int16).max/4, duration=1.0):
        super().__init__(frequency=frequency, sampleRate=sampleRate, amplitude=amplitude, duration=duration)
        self._samples = self.generateWave()
        self._gainedSamples = self._samples

    
    def generateWave(self):
        samples = np.sin(self._stepSize * self._time)
        for x in self._time:
            if samples[x] >= 0:
                samples[x] = self._amplitude
            else:
                samples[x] = -self._amplitude

        return self.crop_samples(samples)


#TRIANGLE OSCILLATOR
#Source: https://stackoverflow.com/questions/1073606/is-there-a-one-line-function-that-generates-a-triangle-wave
class TriangleOscillator(Oscillator):
    def __init__(self, frequency=440, sampleRate=48000, amplitude=np.iinfo(np.int16).max/4, duration=1.0):
        super().__init__(frequency=frequency, sampleRate=sampleRate, amplitude=amplitude, duration=duration)
        self._samples = self.generateWave()
        self._gainedSamples = self._samples

    def generateWave(self):
        samples = np.empty(int(self._sampleRate*self._duration), dtype=float)

        #half-period
        hp = (1 / self._frequency) / 2

        #double the amplitude
        da = self._amplitude * 2

        for x in self._time:
            samples[x] =  da/hp * (hp - np.abs(np.mod(x/self._sampleRate + hp/2,(2*hp))-hp)) - self._amplitude
        
        return self.crop_samples(samples)

#SAW TOOTH OSCILLATOR
class SawtoothOscillator(Oscillator):
    def __init__(self, frequency=440, sampleRate=48000, amplitude=np.iinfo(np.int16).max/4, duration=1.0):
        super().__init__(frequency=frequency, sampleRate=sampleRate, amplitude=amplitude, duration=duration)
        self._samples = self.generateWave()
        self._gainedSamples = self._samples

    def generateWave(self):
        samples = np.arange(self._sampleRate * self._duration)

        for x in self._time:
            samples[x] = 2 * np.fmod(((x * self._frequency * self._amplitude)/ self._sampleRate)+self._amplitude/2, self._amplitude) - self._amplitude

        return self.crop_samples(samples)
