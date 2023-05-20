from scipy.fftpack import fft
from scipy.io import wavfile # get the api
import plotly.graph_objects as go
import numpy as np
import os
import pyaudio



# Configuration
FPS = 30
FFT_WINDOW_SECONDS = 1 # how many seconds of audio make up an FFT window
AMP_THRESHOLD = 0
DIFF_THRESHOLD = 0

# Note range to display
FREQ_MIN = 10
FREQ_MAX = 1000

CHUNK = 1024
CHANNELS = 1
RATE = 44100

# Notes to display
TOP_NOTES = 1

# Names of the notes
NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def find_notes(audio, fs):
  FRAME_STEP = int(fs / FPS) # audio samples per video frame
  FFT_WINDOW_SIZE = int(fs * FFT_WINDOW_SECONDS)
  FRAME_OFFSET = int(FFT_WINDOW_SIZE / FRAME_STEP)
  # print(FFT_WINDOW_SIZE)

  xf = np.fft.rfftfreq(FFT_WINDOW_SIZE, 1 / fs)
  final_notes = []
  final_freqs = []


  def find_top_notes(fft, num):
    if np.max(fft.real) < 0.001:
      return []

    lst = [x for x in enumerate(fft.real)]
    lst = sorted(lst, key=lambda x: x[1], reverse=True)

    idx = 0
    found = []
    found_note = set()
    while idx < len(lst) and len(found) < num:
      f = xf[lst[idx][0]]
      y = lst[idx][1]
      n = freq_to_number(f)
      n0 = int(round(n))
      name = note_name(n0)

      if name not in found_note:
        found_note.add(name)
        s = [f, note_name(n0), y]
        found.append(s)
      idx += 1

    return found

  def freq_to_number(f): return 69 + 12 * np.log2(f / 220.0)
  def note_name(n): return NOTE_NAMES[n % 12] + str(int(n / 12 - 2))

  # Hanning window function
  window = 0.5 * (1 - np.cos(np.linspace(0, 2*np.pi, FFT_WINDOW_SIZE, False)))

  # sample_buffer = np.zeros(FFT_WINDOW_SIZE, dtype=np.float32)
  # buffer_index = 0



  # for i in range(len(audio)):
  #   #print(buffer_index)
  #   sample_buffer[buffer_index] = audio[i]
  #   buffer_index += 1

  #   if buffer_index >= FFT_WINDOW_SIZE:
  #     print('udalo sie')
  #     sample = sample_buffer.copy()


  if len(audio) < FFT_WINDOW_SIZE:
    audio = np.pad(audio, (0, FFT_WINDOW_SIZE - len(audio)), 'constant')

    for i in range(0, len(audio), FRAME_OFFSET):
      sample = audio[i:i+FFT_WINDOW_SIZE]


    if len(audio)< FFT_WINDOW_SIZE:
     audio = np.pad(audio, (0, FFT_WINDOW_SIZE - len(audio)), 'constant')


    fft = np.fft.rfft(sample * window)
    fft_normalized = np.abs(fft) / (np.max(np.abs(fft)) + np.finfo(float).eps)

    s = find_top_notes(fft_normalized, TOP_NOTES)
    if s:
      print('!!!!!')
      if s[0][0] > 81 and s[0][0] < 660:
        frame_dict = {
            'amp': s[0][2],
            'note': s[0][1],
            'freq': s[0][0]
          }
        final_notes.append(frame_dict['note'])
        final_freqs.append(frame_dict['freq'])

      # sample_buffer[:buffer_index - FRAME_STEP] = sample_buffer[FRAME_OFFSET:]
      # buffer_index-=FRAME_STEP

  return final_freqs, final_notes



# def creating_tab(final_notes):
#   E4_row = ['E4', 'F4', 'F#4', 'G4', 'G#4', 'A4', 'A#4', 'B4', 'C5', 'C#5', 'D5', 'D#5', 'E5']
#   B3_row = ['B3', 'C4', 'C#4', 'D4', 'D#4', 'E4', 'F4', 'F#4', 'G4', 'G#4', 'A4', 'A#4', 'B4']
#   G3_row = ['G3', 'G#3', 'A3', 'A#3', 'B3', 'C4', 'C#4', 'D4', 'D#4', 'E4', 'F4', 'F#4', 'G4']
#   D3_row = ['D3', 'D#3', 'E3', 'F3', 'F#3', 'G3', 'G#3', 'A3', 'A#3', 'B3', 'C4', 'C#4', 'D4']
#   A2_row = ['A2', 'A#2', 'B2', 'C3', 'C#3', 'D3', 'D#3', 'E3', 'F3', 'F#3', 'G3', 'G#3', 'A3']
#   E2_row = ['E2', 'F2', 'F#2', 'G2', 'G#2', 'A2', 'A#2', 'B2', 'C3', 'C#3', 'D3', 'D#3', 'E3']

#   row_table = [E4_row, B3_row, G3_row, D3_row, A2_row, E2_row]

#   final_tab = ''
#   dict_of_tuples = []

#   #creating dict_of_tuples with ordered note names with number of string that they can be played on
#   for note in final_notes:
#     for i in range(0,6):
#       if note in row_table[i]:
#         dict_of_tuples.append((note, i))
#         break

#   #creating lines that will be summed as tab
#   E4 = 'E4|--'
#   B3 = 'B3|--'
#   G3 = 'G3|--'
#   D3 = 'D3|--'
#   A2 = 'A2|--'
#   E2 = 'E2|--'
#   final_tab_table = [E4, B3, G3, D3, A2, E2]

#   for tup in dict_of_tuples:
#     final_tab_table[tup[1]] = final_tab_table[tup[1]] + str(row_table[tup[1]].index(tup[0])) + '--'
#     for i in range(0, 6):
#       if i != tup[1]:
#         if (row_table[tup[1]].index(tup[0])>9):
#           final_tab_table[i] = final_tab_table[i] + '----'
#         else:
#           final_tab_table[i]=final_tab_table[i] + '---'

#   #summing lines to tab
#   for line in final_tab_table:
#     final_tab = final_tab + line + '\n'

#   #print(dict_of_tuples)

#   return final_tab

# def writing_to_txt_file(tabulature):
#   exists = True
#   i = 1
#   while os.path.exists(f'tabs/tab{i}.txt'):
#     i+=1

#   with open(f'tabs/tab{i}.txt', 'w') as tab:
#     tab.write(tabulature)

# #writing_to_txt_file(creating_tab(final_notes))


