import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.io import wavfile
import plotly.graph_objects as go
import numpy as np
import numpy as np
import tqdm
import librosa

# Configuration
FPS = 30
FFT_WINDOW_SECONDS = 0.3  # how many seconds of audio make up an FFT window
AMP_THRESHOLD = 0.1
DIFF_THRESHOLD = 0.1

# Note range to display
FREQ_MIN = 10
FREQ_MAX = 1000

# Notes to display
TOP_NOTES = 1

# Names of the notes
NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def find_notes(audio_chunk):
    fs = 44100  # assuming a sample rate of 44100, you can modify this according to your audio data
    FRAME_STEP = (fs / FPS)  # audio samples per video frame
    FFT_WINDOW_SIZE = int(fs * FFT_WINDOW_SECONDS)
    AUDIO_LENGTH = len(audio_chunk) / fs

    def extract_sample(audio, frame_number):
        begin = int(frame_number * FRAME_STEP)
        end = int(begin + FFT_WINDOW_SIZE)

        if end > len(audio):
            end = len(audio)

        sample = audio[begin:end]

        # Padding with zeros if the sample is smaller than the window size
        if len(sample) < FFT_WINDOW_SIZE:
            pad_size = FFT_WINDOW_SIZE - len(sample)
            sample = np.concatenate([sample, np.zeros(pad_size)])

        return sample

    def find_top_notes(fft, num):
        if np.max(fft.real) < 0.001:
            return []

        lst = [x for x in enumerate(fft.real)]
        lst = sorted(lst, key=lambda x: x[1], reverse=True)

        idx = 0
        found = []
        found_note = set()
        while (idx < len(lst)) and (len(found) < num):
            f = xf[lst[idx][0]]
            y = lst[idx][1]
            n = librosa.hz_to_midi(f)
            if np.isfinite(n):
                n0 = int(round(n))
                name = librosa.midi_to_note(n0)

                if name not in found_note:
                    found_note.add(name)
                    s = [f, name, y]
                    found.append(s)
            idx += 1

        return found

    # def freq_to_number(f): return 69 + 12 * np.log2(f / 220.0)
    # def number_to_freq(n): return 220 * 2.0 ** ((n - 69) / 12.0)
    # def note_name(n): return NOTE_NAMES[n % 12] + str(int(n / 12 - 2))

    # Hanning window function
    window = 0.5 * (1 - np.cos(np.linspace(0, 2 * np.pi, FFT_WINDOW_SIZE, False)))

    xf = np.fft.rfftfreq(FFT_WINDOW_SIZE, 1 / fs)
    FRAME_COUNT = int(AUDIO_LENGTH * FPS)
    FRAME_OFFSET = int(FFT_WINDOW_SIZE / FRAME_COUNT) if FRAME_COUNT != 0 else 0  # Avoid division by zero

    # Pass 1, find out the maximum amplitude so we can scale.
    mx = 0
    for frame_number in range(FRAME_COUNT):
        sample = extract_sample(audio_chunk, frame_number)

        fft = np.fft.rfft(sample * window)
        fft = np.abs(fft).real
        mx = max(np.max(fft), mx)

    print(f"Max amplitude: {mx}")
    final_dict = []

    # Pass 2, produce the animation
    for frame_number in tqdm.tqdm(range(FRAME_COUNT)):
        sample = extract_sample(audio_chunk, frame_number)

        fft = np.fft.rfft(sample * window)
        fft = np.abs(fft) / mx

        s = find_top_notes(fft, TOP_NOTES)
        if s:
            if s[0][0] > 81 and s[0][0] < 660:
                frame_dict = {
                    'amp': s[0][2],
                    'note': s[0][1],
                    'freq': s[0][0]
                }

                final_dict.append(frame_dict)

    final_freqs = []
    final_notes = []
    for i, item in enumerate(final_dict):
        if i > 1 and i < len(final_dict) - 2:
            if item['amp'] > AMP_THRESHOLD:
                if item['amp'] > final_dict[i - 1]['amp'] and item['amp'] > final_dict[i + 1]['amp']:
                    final_notes.append(item['note'])
                    final_freqs.append(item['freq'])

    return final_notes ,final_freqs

