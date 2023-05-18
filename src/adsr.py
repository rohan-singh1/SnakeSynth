'''Design inspired by 
https://python.plainenglish.io/build-your-own-python-synthesizer-part-2-66396f6dad81'''

class ADSREnvelope:
    def __init__(self, attackDuration=0.05, decayDuration=0.2, sustainLevel=0.7, releaseDuration=0.3, sampleRate=48000):
        self._attack = attackDuration
        self._decay = decayDuration
        self._sustain = sustainLevel
        self._release = releaseDuration
        self._sampleRate = sampleRate
    

        
