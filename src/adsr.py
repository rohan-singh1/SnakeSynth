'''Design inspired by 
https://python.plainenglish.io/build-your-own-python-synthesizer-part-2-66396f6dad81'''

from oscillator import SineOscillator
import matplotlib.pyplot as plt
import numpy as np
import enum


DEFAULT_MS = 0.1

class State(enum.Enum):
    IDLE = 0
    ATTACK = 1
    DECAY = 2
    SUSTAIN = 3
    RELEASE = 4

import numpy as np
class ADSREnvelope:
    def __init__(self, attack_duration=1, decay_duration=2, sustain_level=8, release_duration=5, sample_rate=48000):
        self._attack = attack_duration * DEFAULT_MS
        self._decay = decay_duration * DEFAULT_MS
        self._sustain = sustain_level * DEFAULT_MS
        self._release = release_duration * DEFAULT_MS
        self._sample_rate = sample_rate
        self._envelope = np.zeros(sample_rate) #empty envelope
        self._state = State

    def update_state(self, state):
        self._state = State(state)

    def update_attack(self, attack):
        self._attack = attack
    
    def update_decay(self, decay):
        self._decay = decay
    
    def update_sustain(self, sustain):
        self._sustain = sustain
        
    def update_release(self, release):
        self._release = release
    
    def create_envelope(self, wave):
        #Not sure I need this variable...
        #duration = len(wave) / self._sample_rate

        attack_samples = int(self._attack * self._sample_rate)
        decay_samples = int(self._decay * self._sample_rate)
        release_samples = int(self._release * self._sample_rate)
        sustain_samples = max(len(wave) - attack_samples - decay_samples - release_samples, 0)

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
    
if __name__ == "__main__":
    sine = SineOscillator()
    sine_wave = sine.generate_wave()
    adsr = ADSREnvelope(attack_duration=1, decay_duration=1, sustain_level=5, release_duration=1)
    envelope = adsr.create_envelope(sine_wave)
    sine_wave_with_envelope = sine_wave * envelope

    # Plot the wave shapes with ADSR envelope
    plt.figure(figsize=(10, 8))

    plt.subplot(4, 1, 1)
    plt.plot(sine_wave)
    plt.title('Sine Wave')
    plt.xlabel('Sample')
    plt.ylabel('Amplitude')

    plt.subplot(4, 1, 1)
    plt.plot(sine_wave_with_envelope)
    plt.title('Sine Wave with ADSR Envelope')
    plt.xlabel('Sample')
    plt.ylabel('Amplitude')

    #plt.tight_layout()
    plt.show()
