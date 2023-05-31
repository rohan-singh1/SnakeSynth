'''Design inspired by 
https://python.plainenglish.io/build-your-own-python-synthesizer-part-2-66396f6dad81'''

from oscillator import SineOscillator
import matplotlib.pyplot as plt
import numpy as np
import enum
import sounddevice as sd

DEFAULT_MS = 0.05

class State(enum.Enum):
    IDLE = 0
    ATTACK = 1
    DECAY = 2
    SUSTAIN = 3
    RELEASE = 4

import numpy as np
class ADSREnvelope:
    def __init__(self, attack_duration=.5, decay_duration=1, sustain_level=1, release_duration=1, sample_rate=48000):
        self._sample_rate = sample_rate
        self._state = State.IDLE
        self._pos = 0

        self._attack_samples = int(attack_duration * DEFAULT_MS * sample_rate)
        self._decay_samples = int(decay_duration * DEFAULT_MS * sample_rate)
        self._sustain = sustain_level * DEFAULT_MS
        self._release_samples = int(release_duration * DEFAULT_MS * sample_rate)

        self._envelope = np.zeros(sample_rate) #empty envelope
        self._attack_env = self.create_attack_envelope()
        self._decay_env = self.create_decay_envelope()
        self._release_env = self.create_release_envelope()

    def update_state(self, state):
        self._pos = 0
        self._state = state

    def update_attack(self, attack):
        self._attack_samples = int(attack * DEFAULT_MS * self._sample_rate)
        self._attack_env = self.create_attack_envelope()
    
    def update_decay(self, decay):
        self._decay_samples = int(decay * DEFAULT_MS * self._sample_rate)
        self._decay_env = self.create_decay_envelope()
    
    def update_sustain(self, sustain):
        self._sustain = sustain
        
    def update_release(self, release):
        self._release_samples = int(release * DEFAULT_MS * self._sample_rate)
        self._release_env = self.create_release_envelope()

    def process(self, sample):
        #takes in a sample, process based on state, return sample with envelope applied
        if self._state == State.ATTACK:
            output = sample * self._attack_env[self._pos]
            self._pos += 1
            if self._pos >= self._attack_samples:
                self.update_state(State.DECAY)
            return output
        
        elif self._state == State.DECAY:
            output = sample * self._decay_env[self._pos]
            self._pos += 1
            if self._pos >= self._decay_samples:
                self.update_state(State.SUSTAIN)
            return output
        
        elif self._state == State.SUSTAIN:
            return sample *  self._sustain
        
        elif self._state == State.RELEASE:
            output = sample * self._release_env[self._pos]
            self._pos += 1
            if self._pos >= self._release_samples:
                self.update_state(State.IDLE)
            return output
        
    def create_attack_envelope(self):
        return np.linspace(0,1,self._attack_samples)
    
    def create_decay_envelope(self):
        return np.linspace(1,self._sustain,self._decay_samples)
    
    def create_release_envelope(self):
        return np.linspace(self._sustain,0,self._release_samples)

