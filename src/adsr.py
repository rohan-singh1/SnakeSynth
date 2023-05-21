import numpy as np
import sounddevice as sd
import threading
import keyboard

# Global default variables for ADSR parameters
attack_time = 1.0
decay_time = 0.6
sustain_level = 0.5
release_time = 1.0
key_pressed = False  # Flag to track if a key has been pressed

def apply_adsr(signal, sample_rate):
    num_samples = len(signal)
    time = np.linspace(0, num_samples/sample_rate, num_samples)
    envelope = np.ones_like(signal)

    if attack_time > 0.0:
        attack_samples = int(attack_time * sample_rate)
        envelope[:attack_samples] = np.linspace(0, 1, attack_samples)[:num_samples]

    if decay_time > 0.0:
        decay_samples = int(decay_time * sample_rate)
        if attack_time > 0.0:
            decay_end = min(attack_samples + decay_samples, num_samples)
            envelope[attack_samples:decay_end] = np.linspace(1, sustain_level, decay_end - attack_samples)
        else:
            envelope[:decay_samples] = np.linspace(1, sustain_level, decay_samples)[:num_samples]

    release_samples = int(release_time * sample_rate)
    envelope[-release_samples:] = np.linspace(sustain_level, 0, release_samples)[-num_samples:]

    return signal * envelope

""" debug tone for standalone ADSR development 
def play_tone():
    duration = 2.0  # Duration of each tone in seconds
    sample_rate = 44100  # Sample rate in Hz

    while True:
        # Generate a simple sine wave signal
        frequency = 440  # Frequency of the sine wave in Hz
        time = np.linspace(0, duration, int(sample_rate * duration))
        signal = np.sin(2 * np.pi * frequency * time)

        # Apply ADSR envelope effect
        output_signal = apply_adsr(signal, sample_rate)

        # Play the signal with the ADSR envelope applied
        sd.play(output_signal, sample_rate)

        # Wait for the playback to finish
        sd.wait()
"""

def dynamic_parameter_updates():
    global attack_time, decay_time, sustain_level, release_time, key_pressed
    while True:
        if keyboard.is_pressed('a'):
            if not key_pressed:
                attack_time += 0.1
                attack_time = min(attack_time, 10.0)  # Limit to a maximum value of 10.0
                print(f"Attack time: {attack_time} (Valid range: 0.0 - 10.0)")
                key_pressed = True
        elif keyboard.is_pressed('s'):
            if not key_pressed:
                attack_time = max(attack_time - 0.1, 0.0)
                print(f"Attack time: {attack_time} (Valid range: 0.0 - 10.0)")
                key_pressed = True
        elif keyboard.is_pressed('d'):
            if not key_pressed:
                decay_time += 0.1
                decay_time = min(decay_time, 10.0)  # Limit to a maximum value of 10.0
                print(f"Decay time: {decay_time} (Valid range: 0.0 - 10.0)")
                key_pressed = True
        elif keyboard.is_pressed('f'):
            if not key_pressed:
                decay_time = max(decay_time - 0.1, 0.0)
                print(f"Decay time: {decay_time} (Valid range: 0.0 - 10.0)")
                key_pressed = True
        elif keyboard.is_pressed('g'):
            if not key_pressed:
                sustain_level += 0.1
                sustain_level = min(sustain_level, 1.0)  # Limit to a maximum value of 1.0
                print(f"Sustain level: {sustain_level} (Valid range: 0.0 - 1.0)")
                key_pressed = True
        elif keyboard.is_pressed('h'):
            if not key_pressed:
                sustain_level = max(sustain_level - 0.1, 0.0)
                print(f"Sustain level: {sustain_level} (Valid range: 0.0 - 1.0)")
                key_pressed = True
        elif keyboard.is_pressed('j'):
            if not key_pressed:
                release_time += 0.1
                release_time = min(release_time, 10.0)  # Limit to a maximum value of 10.0
                print(f"Release time: {release_time} (Valid range: 0.0 - 10.0)")
                key_pressed = True
        elif keyboard.is_pressed('k'):
            if not key_pressed:
                release_time = max(release_time - 0.1, 0.0)
                print(f"Release time: {release_time} (Valid range: 0.0 - 10.0)")
                key_pressed = True
        else:
            key_pressed = False  # Reset the flag if no key is pressed

# Create separate threads for playing the tone and updating parameters
# tone_thread = threading.Thread(target=play_tone)
param_thread = threading.Thread(target=dynamic_parameter_updates)

tone_thread.start()
param_thread.start()
