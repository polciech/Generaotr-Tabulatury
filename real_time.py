import pyaudio
import numpy as np
from rt import find_notes

# Configuration
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# Initialize PyAudio
audio = pyaudio.PyAudio()
freqs=[]

# Open audio stream
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

# Start the stream
stream.start_stream()

try:
    while True:
        # Read audio data from the stream
        data = stream.read(CHUNK)

        # Convert the audio data to numpy array
        audio_np = np.frombuffer(data, dtype=np.int16)

        # Process the audio frame using the find_notes function
        final_freqs = find_notes(audio_np, RATE)
        # Do something with the final_notes and final_freqs


except KeyboardInterrupt:
    # Stop the stream when interrupted
    stream.stop_stream()
    stream.close()
    audio.terminate()
