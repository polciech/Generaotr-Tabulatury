import numpy as np
import sounddevice as sd

# Set the sample rate and duration
sample_rate = 44100 # in Hz
duration = 3 # in seconds

# Define the notes and their frequencies
notes = {
    'C4': 261.63,
    'D4': 293.66,
    'E4': 329.63,
    'F4': 349.23,
    'G4': 392.00,
    'A4': 440.00,
    'B4': 493.88,
    'C5': 523.25
}

# Define a function to generate a sawtooth wave for a given frequency
def generate_sawtooth_wave(frequency, duration, sample_rate):
    # Calculate the number of samples
    num_samples = duration * sample_rate

    # Calculate the time array
    time_array = np.arange(num_samples) / sample_rate

    # Calculate the sawtooth wave
    sawtooth_wave = 2 * (frequency * time_array - np.floor(0.5 + frequency * time_array))

    # Normalize the waveform
    sawtooth_wave /= np.max(np.abs(sawtooth_wave))

    return sawtooth_wave

# Define a function to generate a square wave for a given frequency
def generate_square_wave(frequency, duration, sample_rate):
    # Calculate the number of samples
    num_samples = duration * sample_rate

    # Calculate the time array
    time_array = np.arange(num_samples) / sample_rate

    # Calculate the square wave
    square_wave = np.sign(np.sin(2 * np.pi * frequency * time_array))

    # Normalize the waveform
    square_wave /= np.max(np.abs(square_wave))

    return square_wave

# Define a function to generate a sine wave for a given frequency
def generate_sine_wave(frequency, duration, sample_rate):
    # Calculate the number of samples
    num_samples = duration * sample_rate

    # Calculate the time array
    time_array = np.arange(num_samples) / sample_rate

    # Calculate the sine wave
    sine_wave = np.sin(2 * np.pi * frequency * time_array)

    # Normalize the waveform
    sine_wave /= np.max(np.abs(sine_wave))

    return sine_wave

# Generate the sawtooth, square, and sine waves for a given note
note = 'C4'
frequency = notes[note]
sawtooth_wave = generate_sawtooth_wave(frequency, duration, sample_rate)
square_wave = generate_square_wave(frequency, duration, sample_rate)
sine_wave = generate_sine_wave(frequency, duration, sample_rate)

# Add the waveforms together and play using sounddevice
combined_wave = sawtooth_wave + sine_wave + square_wave
sd.play(combined_wave, sample_rate)
sd.wait() # Wait until the waveform has finished playing
