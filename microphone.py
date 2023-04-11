import pyaudio
import wave
import librosa
import librosa.display
import matplotlib.pyplot as plt
from librosa.display import matplotlib
import numpy as np
from IPython.display import Audio, IFrame, display
from scipy.io import wavfile
from scipy.fftpack import fft
from testowy import find_notes, creating_tab, writing_to_txt_file


#paramtetry nagrania
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

def record():

	#inicjowanie sesji audio
	audio = pyaudio.PyAudio()


	info = audio.get_host_api_info_by_index(0)
	numdevices = info.get('deviceCount')

	for i in range(0, numdevices):
		if (audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
			print("Input Device id ", i, " - ", audio.get_device_info_by_host_api_device_index(0, i).get('name'))
	input_id = int(input("Podaj wejście: "))

	stream = audio.open(format= FORMAT, channels=CHANNELS, rate= RATE, frames_per_buffer=CHUNK, input= True)

	print('starting recording')

	frames = []

	try:
		while True:
			data = stream.read(CHUNK)
			frames.append(data)
	except KeyboardInterrupt:
		print("done recording")
	except Exception as e:
		print(str(e))

	sample_width = audio.get_sample_size(FORMAT)

	#zamykanie sesji nagrywania
	stream.stop_stream()
	stream.close()
	audio.terminate()

	return sample_width, frames

#zapisywanie do pliku
def record_to_file(filepath):
	wf = wave.open(filepath, 'wb')
	wf.setnchannels(CHANNELS)
	sample_width, frames = record()
	wf.setsampwidth(sample_width)
	wf.setframerate(RATE)
	wf.writeframes(b''.join(frames))
	wf.close()





record_to_file('recordings/recording.wav')
e_file1 = '/recordings/recording.wav'



# FILE,RATE = librosa.load(e_file1, mono=True, sr=RATE, offset=0, duration=librosa.get_duration(sr = RATE, path='recording.wav'))

# plot1 = plt.subplot(2,1,1)
# librosa.display.waveshow(FILE,sr=RATE)

# S1 = librosa.feature.melspectrogram(y=FILE, sr=RATE, n_mels=64)
# D1 = librosa.power_to_db(S1, ref=np.max)
# plot2 = plt.subplot(2,1,2)
# librosa.display.specshow(D1, x_axis='time', y_axis='mel')
# plt.show()

writing_to_txt_file(creating_tab(find_notes('\recordings\recording.wav')))