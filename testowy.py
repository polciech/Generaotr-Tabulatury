import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.io import wavfile # get the api
import plotly.graph_objects as go
import numpy as np
import numpy as np
import tqdm
import os
import librosa


# Configuration
FPS = 30
FFT_WINDOW_SECONDS = 0.7 # how many seconds of audio make up an FFT window
AMP_THRESHOLD = 0.1
DIFF_THRESHOLD = 0.1

# Note range to display
FREQ_MIN = 0
FREQ_MAX = 1000

# Notes to display
TOP_NOTES = 1

# Names of the notes
NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

def find_notes(FILE_NAME):
  fs, data = wavfile.read(FILE_NAME) # load the data
  audio = data.T[0] # this is a two channel soundtrack, get the first track
  FRAME_STEP = (fs / FPS) # audio samples per video frame
  FFT_WINDOW_SIZE = int(fs * FFT_WINDOW_SECONDS)
  AUDIO_LENGTH = len(audio)/fs

  def extract_sample(audio, frame_number):
    end = frame_number * FRAME_OFFSET
    begin = int(end - FFT_WINDOW_SIZE)

    if end == 0:
      # We have no audio yet, return all zeros (very beginning)
      return np.zeros((np.abs(begin)),dtype=float)
    elif begin<0:
      # We have some audio, padd with zeros
      return np.concatenate([np.zeros((np.abs(begin)),dtype=float),audio[0:end]])
    else:
      # Usually this happens, return the next sample
      return audio[begin:end]

  def find_top_notes(fft,num):
    if np.max(fft.real)<0.001:
      return []

    lst = [x for x in enumerate(fft.real)]
    lst = sorted(lst, key=lambda x: x[1],reverse=True)

    idx = 0
    found = []
    found_note = set()
    while( (idx<len(lst)) and (len(found)<num) ):
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

  def freq_to_number(f): return 69 + 12*np.log2(f/220.0)
  def number_to_freq(n): return 220 * 2.0**((n-69)/12.0)
  def note_name(n): return NOTE_NAMES[n % 12] + str(int(n/12 - 2))

  # Hanning window function
  window = 0.5 * (1 - np.cos(np.linspace(0, 2*np.pi, FFT_WINDOW_SIZE, False)))

  xf = np.fft.rfftfreq(FFT_WINDOW_SIZE, 1/fs)
  FRAME_COUNT = int(AUDIO_LENGTH*FPS)
  FRAME_OFFSET = int(len(audio)/FRAME_COUNT)

  # Pass 1, find out the maximum amplitude so we can scale.
  mx = 0
  for frame_number in range(FRAME_COUNT):
    sample = extract_sample(audio, frame_number)

    fft = np.fft.rfft(sample * window)
    fft = np.abs(fft).real
    mx = max(np.max(fft),mx)

  print(f"Max amplitude: {mx}")
  final_dict = []


  # Pass 2, produce the animation
  for frame_number in tqdm.tqdm(range(FRAME_COUNT)):
    sample = extract_sample(audio, frame_number)

    fft = np.fft.rfft(sample * window)
    fft = np.abs(fft) / mx

    s = find_top_notes(fft,TOP_NOTES)
    if s:
      if s[0][0]> 81 and s[0][0]< 660:
        frame_dict = {'amp':s[0][2],
                  'note':s[0][1],
                 'freq':s[0][0]}

        final_dict.append(frame_dict)

  final_notes=[]
  final_freqs=[]
  for i,item in enumerate(final_dict):
   if i>1 and i<len(final_dict)-2:
     if item['amp']>AMP_THRESHOLD:
       if item['amp'] > final_dict[i-1]['amp'] and item['amp']>final_dict[i+1]['amp']:
         final_notes.append(item['note'])
         final_freqs.append(item['freq'])
  return final_notes, final_freqs

nuty = ['D3', 'C3', 'G2', 'E5', 'A3']

def creating_tab(final_notes, strojenie_index):
  #NOTES_TABLE = ['E4', 'F4', 'F#4', 'G4', 'G#4', 'A4', 'A#4', 'B4', 'C5', 'C#5', 'D5', 'D#5', 'E5'
  #              ,'B3', 'C4', 'C#4', 'D4', 'D#4', 'E4', 'F4', 'F#4', 'G4', 'G#4', 'A4', 'A#4', 'B4'
  #              ,'G3', 'G#3', 'A3', 'A#3', 'B3', 'C4', 'C#4', 'D4', 'D#4', 'E4', 'F4', 'F#4', 'G4'
  #              ,'D3', 'D#3', 'E3', 'F3', 'F#3', 'G3', 'G#3', 'A3', 'A#3', 'B3', 'C4', 'C#4', 'D4'
  #              ,'A2', 'A#2', 'B2', 'C3', 'C#3', 'D3', 'D#3', 'E3', 'F3', 'F#3', 'G3', 'G#3', 'A3'
  #              ,'E2', 'F2', 'F#2', 'G2', 'G#2', 'A2', 'A#2', 'B2', 'C3', 'C#3', 'D3', 'D#3', 'E3']
  
  strojenie_lists = [['E5', 'B4', 'G4', 'D4', 'A3', 'E3'],  #Standardowy strój  0
                     ['E5', 'B4', 'G4', 'D4', 'A3', 'D3'],  #Drop D             1
                     ['D5', 'A4', 'G4', 'D4', 'A3', 'D3'],  #DADGAD             2
                     ['D5', 'B4', 'G4', 'D4', 'A3', 'D3'],  #Double Drop D      3
                     ['C5', 'C5', 'G4', 'D4', 'A3', 'D3'],  #D7sus4             4
                     ['D5', 'A4', 'F#4', 'D4', 'A3', 'D3'], #Open D Major       5
                     ['E5', 'C4', 'F4', 'C4', 'D3', 'C3'],  #Cmaj9sus4          6
                     ['A#4', 'F4', 'E4', 'A#3', 'G3', 'C3'],#Cmaj7sus4          7
                     ['F5', 'C4', 'G4', 'C4', 'G3', 'C3'],  #Csus4              8
                     ['E5', 'A4', 'E4', 'C#4', 'A3', 'E3'], #Open A Major       9
                     ['E5', 'B4', 'G#4', 'E4', 'B3', 'E3'], #Open E Major       10
                     ['E5', 'A4', 'G4', 'E4', 'B3', 'E3'],  #E Minor Sus4       11
                     ['E5', 'A4', 'E4', 'D4', 'A3', 'E3'],  #Double E Double A  12
                     ['D5', 'B4', 'G4', 'D4', 'G3', 'D3']]  #Open G Major       13

  NOTES_TABLE = ['C2', 'C#2', 'D2', 'D#2','E2', 'F2', 'F#2', 'G2', 'G#2', 'A2', 'A#2', 'B2', 'C3', 'C#3',
                'D3', 'D#3', 'E3', 'F3', 'F#3', 'G3', 'G#3', 'A3', 'A#3', 'B3', 'C4', 'C#4', 'D4', 'D#4', 
                'E4', 'F4', 'F#4', 'G4', 'G#4', 'A4', 'A#4', 'B4', 'C5', 'C#5', 'D5', 'D#5', 'E5', 'F5', 'F#5', 'G5', 'G#5', 'A5', 'A#5', 'B5', 'C6', 'C#6', 'D6', 'D#6', 'E6', 'F6']  

  row_0 = []
  row_1 = []
  row_2 = []
  row_3 = []
  row_4 = []
  row_5 = []

  row_table = [row_0, row_1, row_2, row_3, row_4, row_5]
  
  #creating lines that will be summed as tab
  SN_1 = '|--'
  SN_2 = '|--'
  SN_3 = '|--'
  SN_4 = '|--'
  SN_5 = '|--'
  SN_6 = '|--'
  final_tab_table = [SN_1, SN_2, SN_3, SN_4, SN_5, SN_6]
  
  for STARTING_NOTE in strojenie_lists[strojenie_index]:
    row_table[strojenie_lists[strojenie_index].index(STARTING_NOTE)] = NOTES_TABLE[NOTES_TABLE.index(STARTING_NOTE): NOTES_TABLE.index(STARTING_NOTE)+13]
    if len(STARTING_NOTE) > 2:
      final_tab_table[strojenie_lists[strojenie_index].index(STARTING_NOTE)] = STARTING_NOTE + final_tab_table[strojenie_lists[strojenie_index].index(STARTING_NOTE)]
    else:
      final_tab_table[strojenie_lists[strojenie_index].index(STARTING_NOTE)] = ' ' + STARTING_NOTE + final_tab_table[strojenie_lists[strojenie_index].index(STARTING_NOTE)]
      
      
  final_tab = ''
  table_of_tables = []

  #creating table_of_tables with ordered note names with number of string that they can be played on
  for note in final_notes:
    for i in range(0,6):
      if note in row_table[i]:
        table_of_tables.append([note, i, row_table[i].index(note)])
        break
  
  
  #correcting function
  for tab in table_of_tables:
    for i in range(0, 6):
      if table_of_tables.index(tab) == 0:
        continue
      else:
        if tab[0] in row_table[i]:
          if abs(tab[2] - table_of_tables[table_of_tables.index(tab)-1][2]) > abs(row_table[i].index(tab[0]) - table_of_tables[table_of_tables.index(tab)-1][2]):
            tab[1] = i
            tab[2] = row_table[i].index(tab[0])
          
  
  for tab in table_of_tables:
    final_tab_table[tab[1]] = final_tab_table[tab[1]] + str(tab[2]) + '--'
    for i in range(0, 6):
      if i != tab[1]:
        if (tab[2]>9):
          final_tab_table[i] = final_tab_table[i] + '----'
        else:
          final_tab_table[i]=final_tab_table[i] + '---'

  
  #summing lines to tab
  for line in final_tab_table:
    final_tab = final_tab + line + '\n'

  #print(dict_of_tuples)

  return final_tab

def writing_to_txt_file(tabulature):
  exists = True
  # i = 1
  # while os.path.exists(f'tabs/tab{i}.txt'):
  #   i+=1

  with open(f'tab.txt', 'w') as tab:
    tab.write(tabulature)


