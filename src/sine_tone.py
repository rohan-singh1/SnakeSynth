from scipy.io import wavfile
import numpy as np
import sounddevice as sd


def play_sine (pitch_coefficient):

    # Sine wave generation sourced from:
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.wavfile.write.html

    fs = 48000
    cycles_per_second = 440
    time = np.linspace(0., 1., fs)
    amplitude = np.iinfo(np.int16).max / 4
    sine_wave = amplitude * np.sin(pitch_coefficient * np.pi * cycles_per_second * time)


    # Sound playback sourced from:
    # https://python-sounddevice.readthedocs.io/en/0.4.6/usage.html

    sd.play(sine_wave, fs)

def stop_playing():
    sd.stop()
