'''Design inspired by 
https://python.plainenglish.io/build-your-own-python-synthesizer-part-2-66396f6dad81'''

import numpy as np

class ADSREnvelope:
    def __init__(self, wave, attackDuration=0.05, decayDuration=0.2, sustainLevel=0.7, releaseDuration=0.3, sampleRate=48000):
        self._attack = attackDuration
        self._decay = decayDuration
        self._sustain = sustainLevel
        self._release = releaseDuration
        self._sampleRate = sampleRate
        self._originalWave = wave
        self._envelope = np.ones(self._originalWave) #blank envelope
        self._createEnvelope()
        self._modulatedWave = self.applyEnvelope()
    
    def _createEnvelope(self):
        #Not sure I need this variable...
        #duration = len(self._originalWave) / self._sampleRate
        attackSamples = int(self._attack * self._sampleRate)
        decaySamples = int(self._decay * self._sampleRate)
        releaseSamples = int(self._release * self._sampleRate)
        sustainSamples = len(self._originalWave) - attackSamples - decaySamples - releaseSamples

        self._envelope[:attackSamples] = np.linspace(0, 1, attackSamples)
        self._envelope[attackSamples:attackSamples+decaySamples] = np.linspace(1, self._sustain, decaySamples)
        self._envelope[attackSamples+decaySamples:attackSamples+decaySamples+sustainSamples] = self._sustain
        self._envelope[attackSamples+decaySamples+sustainSamples:] = np.linspace(self._sustain, 0, releaseSamples)
    
    def applyEnvelope(self):
        return self._originalWave * self._envelope
    