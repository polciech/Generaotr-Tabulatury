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
    previous_note = None


    while True:
        audio_data = audio_buffer()
        f = find_notes(audio_data)
        f_size = len(f)
        for i in range(f_size):
            notes.append(f[i])
            print(notes)

