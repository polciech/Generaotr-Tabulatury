import pyaudio
import numpy as np
from buffer import AudioBuffer
from rt_process import find_notes

# Configuration
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# Initialize PyAudio
audio = pyaudio.PyAudio()
freqs=[]

if __name__ == "__main__":
    audio_buffer = AudioBuffer()
    audio_buffer.start()
    notes =[]
    freqs =[]
    previous_note = None


    while True:
        audio_data = audio_buffer()
        note, freq = find_notes(audio_data)
        f_size = len(freq)
        for i in range(f_size):
            if note[i] != previous_note:
                freqs.append(freq[i])
                notes.append(note[i])
                print(notes)
                print(freqs)
                previous_note = note[i]