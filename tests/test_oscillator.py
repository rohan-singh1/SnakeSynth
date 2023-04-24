import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.oscillator import SineOscillator
import numpy as np

def test_sine_oscillator():
    freq = 440
    sampleRate = 48000
    duration = 1.0
    oscillator = SineOscillator(frequency=freq, sampleRate=sampleRate, duration=duration)
    wave = oscillator.generateWave()
    assert len(wave) == sampleRate * duration
    assert np.allclose(wave, np.sin(oscillator._pitchCoefficient * np.pi * freq * oscillator._time) * oscillator._amplitude)