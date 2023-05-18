'''Design inspired by 
https://python.plainenglish.io/build-your-own-python-synthesizer-part-2-66396f6dad81'''

import numpy as np

class ADSREnvelope:
    def __init__(self, attackDuration=0.05, decayDuration=0.2, sustainLevel=0.7, releaseDuration=0.3, sampleRate=48000):
        self._attack = attackDuration
        self._decay = decayDuration
        self._sustain = sustainLevel
        self._release = releaseDuration
        self._sampleRate = sampleRate
    
    def applyEnvelope(self, wave):
        duration = len(wave) / self._sampleRate
        attackSamples = int(self._attack * self._sampleRate)
        decaySamples = int(self._decay * self._sampleRate)
        releaseSamples = int(self._release * self._sampleRate)
        sustainSamples = len(wave) - attackSamples - decaySamples - releaseSamples

        envelope = np.ones(len(wave))
        envelope[:attackSamples] = np.linspace(0, 1, self._attack)
        envelope[attackSamples:attackSamples+decaySamples] = np.linspace(1, self._sustain, self._decay)
        envelope[attackSamples+decaySamples:attackSamples+decaySamples+releaseSamples] = self._sustain
        envelope[attackSamples+decaySamples+releaseSamples:] = np.linspace(self._sustain, 0, self._release)

        return wave * envelope


        
