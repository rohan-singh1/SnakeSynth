from scipy.io import wavfile
import numpy as np
import sounddevice as sd


# sampling frequency needs to be available to all functions 
fs = 48000
amplitude_default = 1    # set a default amplitude for all wave functions 



# Generate the sine wave
def oscillator_sine(freq, dur):
    # Set parameters for the sine wave

    time_array = np.arange(0, dur, 1 / fs)
    sine_wave = np.sin(2 * np.pi * freq * time_array)

    # Apply fade-out effect
    fade_out_duration = 0.05  # in seconds
    fade_out_samples = int(fade_out_duration * fs)
    fade_out_array = np.linspace(1, 0, fade_out_samples)
    sine_wave[-fade_out_samples:] *= fade_out_array

    sd.play(sine_wave, fs)

def play_sine (pitch_coefficient):

    # Sine wave generation sourced from:
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.wavfile.write.html

    
    cycles_per_second = 440
    time = np.linspace(0., 1., fs)
    amplitude = np.iinfo(np.int16).max / 4
    sine_wave = amplitude * np.sin(pitch_coefficient * np.pi * cycles_per_second * time)

    # Sound playback sourced from:
    # https://python-sounddevice.readthedocs.io/en/0.4.6/usage.html

    sd.play(sine_wave, fs)

def stop_playing():
    sd.stop()
