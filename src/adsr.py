'''Design inspired by 
https://python.plainenglish.io/build-your-own-python-synthesizer-part-2-66396f6dad81'''

import numpy as np
class ADSREnvelope:
    def __init__(self, attack_duration=0.1, decay_duration=0.2, sustain_level=0.8, release_duration=0.5, sample_rate=48000):
        self._attack = attack_duration
        self._decay = decay_duration
        self._sustain = sustain_level
        self._release = release_duration
        self._sample_rate = sample_rate
        self._envelope = np.zeros(sample_rate)

    def update_attack(self, attack):
        self._attack = attack
    
    def update_decay(self, decay):
        self._decay = decay
    
    def update_sustain(self, sustain):
        self._sustain = sustain
        
    def update_release(self, release):
        self._release = release
    
    def _create_envelope(self, wave):
        #Not sure I need this variable...
        duration = len(wave) / self._sample_rate
        num_samples = int(self._sample_rate * duration)

        attack_samples = int(self._attack * self._sample_rate)
        decay_samples = int(self._decay * self._sample_rate)
        release_samples = int(self._release * self._sample_rate)
        #sustain_samples = len(self._original_wave) - attack_samples - decay_samples - release_samples
        sustain_samples = max(num_samples - attack_samples - decay_samples - release_samples, 0)

        #self._envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
        #self._envelope[attack_samples:attack_samples+decay_samples] = np.linspace(1, self._sustain, decay_samples)
        #self._envelope[attack_samples+decay_samples:attack_samples+decay_samples+sustain_samples] = self._sustain
        #self._envelope[attack_samples+decay_samples+sustain_samples:] = np.linspace(self._sustain, 0, release_samples)
        # Generate the ADSR envelope by concatenating arrays that represent each phase
        self._envelope = np.concatenate([
        np.linspace(0, 1, attack_samples),                    # Attack phase: linearly increasing from 0 to 1
        np.linspace(1, self._sustain, decay_samples),         # Decay phase: linearly decreasing from 1 to sustain_level
        np.full(sustain_samples, self._sustain),              # Sustain phase: constant sustain_level
        np.linspace(self._sustain, 0, release_samples)         # Release phase: linearly decreasing from sustain_level to 0

        self.apply_envelope(wave)
    ])
    
    def apply_envelope(self, wave):
        normalized_wave = wave / np.max(np.abs(wave)) 
        return normalized_wave * self._envelope
    