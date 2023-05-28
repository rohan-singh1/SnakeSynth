'''Design inspired by 
https://python.plainenglish.io/build-your-own-python-synthesizer-part-2-66396f6dad81'''

DEFAULT_MS = 0.1

import numpy as np
class ADSREnvelope:
    def __init__(self, attack_duration=1, decay_duration=2, sustain_level=8, release_duration=5, sample_rate=48000):
        self._attack = attack_duration * DEFAULT_MS
        self._decay = decay_duration * DEFAULT_MS
        self._sustain = sustain_level * DEFAULT_MS
        self._release = release_duration * DEFAULT_MS
        self._sample_rate = sample_rate
        self._envelope = np.zeros(sample_rate)
        self._is_key_pressed = False

    def update_attack(self, attack):
        self._attack = attack
    
    def update_decay(self, decay):
        self._decay = decay
    
    def update_sustain(self, sustain):
        self._sustain = sustain
        
    def update_release(self, release):
        self._release = release

    def key_pressed(self):
        self._is_key_pressed = True
    
    def key_released(self):
        self._is_key_pressed = False
    
    def create_envelope(self, wave):
        #Not sure I need this variable...
        #duration = len(wave) / self._sample_rate

        attack_samples = int(self._attack * self._sample_rate)
        decay_samples = int(self._decay * self._sample_rate)
        release_samples = int(self._release * self._sample_rate)
        #sustain_samples = len(wave) - attack_samples - decay_samples - release_samples
        sustain_samples = max(len(wave) - attack_samples - decay_samples - release_samples, 0)

        #self._envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
        #self._envelope[attack_samples:attack_samples+decay_samples] = np.linspace(1, self._sustain, decay_samples)
        #self._envelope[attack_samples+decay_samples:attack_samples+decay_samples+sustain_samples] = self._sustain
        #self._envelope[attack_samples+decay_samples+sustain_samples:] = np.linspace(self._sustain, 0, release_samples)
        # Generate the ADSR envelope by concatenating arrays that represent each phase
        self._envelope = np.concatenate([
        np.linspace(0, 1, attack_samples),                    
        np.linspace(1, self._sustain, decay_samples),         
        np.full(sustain_samples, self._sustain),              
        np.linspace(self._sustain, 0, release_samples)         
        ])

        #adjust the length of the envelope using linear interpolation
        if len(self._envelope) != len(wave):
            self._envelope = np.interp(
                np.linspace(0, len(self._envelope) - 1, len(wave)),
                np.arange(len(self._envelope)),
                self._envelope
            )

        return self._envelope
    