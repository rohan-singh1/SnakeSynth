'''Design inspired by 
https://python.plainenglish.io/build-your-own-python-synthesizer-part-2-66396f6dad81'''

from oscillator import SineOscillator
import matplotlib.pyplot as plt
import numpy as np
import enum
import sounddevice as sd

DEFAULT_MS = 0.1

class State(enum.Enum):
    IDLE = 0
    ATTACK = 1
    DECAY = 2
    SUSTAIN = 3
    RELEASE = 4

import numpy as np
class ADSREnvelope:
    def __init__(self, attack_duration=1, decay_duration=2, sustain_level=1, release_duration=5, sample_rate=48000):
        self._attack_samples = int(attack_duration * DEFAULT_MS * sample_rate)
        self._decay_samples = int(decay_duration * DEFAULT_MS * sample_rate)
        self._sustain = sustain_level * DEFAULT_MS
        self._release_samples = int(release_duration * DEFAULT_MS * sample_rate)
        self._sample_rate = sample_rate
        self._envelope = np.zeros(sample_rate) #empty envelope
        self._attack_env = self.create_attack_envelope()
        self._decay_env = self.create_decay_envelope()
        self._release_env = self.create_release_envelope()
        self._state = State.IDLE
        self._pos = 0

    def update_state(self, state):
        self._pos = 0
        self._state = state

    def update_attack(self, attack):
        self._attack = attack
    
    def update_decay(self, decay):
        self._decay = decay
    
    def update_sustain(self, sustain):
        self._sustain = sustain
        
    def update_release(self, release):
        self._release = release

    def process(self, sample):
        #takes in samples, process based on state, return samples with envelope applied
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

    
    def create_envelope(self, wave):
        #Not sure I need this variable...
        #duration = len(wave) / self._sample_rate

        #number of samples of each phase

        # Generate the ADSR envelope by concatenating arrays that represent each phase
        self._envelope = np.concatenate([
        np.linspace(0, 1, self._attack_samples),                    
        np.linspace(1, self._sustain, self._decay_samples),           
        np.linspace(self._sustain, 0, self._release_samples)         
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
    sd.wait()
    sd.play(sine_wave_with_envelope.astype(np.int16), 48000)
    sd.wait()
    plt.show()
