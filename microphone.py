import pyaudio
import wave
import librosa
import librosa.display
import matplotlib.pyplot as plt
from librosa.display import matplotlib
import numpy as np
from IPython.display import Audio, IFrame, display

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


record_to_file('recording.wav')
e_file1 = 'recording.wav'
dur = librosa.get_duration(sr = RATE, path='recording.wav')
print(dur)

FILE,RATE = librosa.load(e_file1, mono=True, sr=RATE, offset=0, duration=dur)

plot1 = plt.subplot(5,1,1)
librosa.display.waveshow(FILE,sr=RATE)

n = len(FILE)
fhat = np.fft.fft(FILE, n) #computes the fft
psd = fhat * np.conj(fhat)/n
freq = (1/(dur)) * np.arange(n) #frequency array
idxs_half = np.arange(1, np.floor(n/2), dtype=np.int32) #first half index

## Filter out noise
threshold = 0.005
psd_idxs = psd > threshold #array of 0 and 1
psd_clean = psd * psd_idxs #zero out all the unnecessary powers
fhat_clean = psd_idxs * fhat #used to retrieve the signal

signal_filtered = np.fft.ifft(fhat_clean) #inverse fourier transform
signal_filtered_real = np.real(signal_filtered)
plot2 = plt.subplot(5,1,2)
plot2.plot(freq[idxs_half], np.abs(psd[idxs_half]), lw=0.5)
plot2.set_xlabel('Frequencies in Hz')
plot2.set_ylabel('Amplitude')
plt.xscale("log")


plot3 = plt.subplot(5,1,3)
plot3.plot(freq[idxs_half], np.abs(psd_clean[idxs_half]), lw=1)
plot3.set_xlabel('Frequencies in Hz')
plot3.set_ylabel('Amplitude')
plt.xscale("log")


S1 = librosa.feature.melspectrogram(y=FILE, sr=RATE, n_mels=64)
D1 = librosa.power_to_db(S1, ref=np.max)
plot4 = plt.subplot(5,1,4)
librosa.display.specshow(D1, x_axis='time', y_axis='mel')

print(signal_filtered)

S2 = librosa.feature.melspectrogram(y=signal_filtered_real, sr=RATE, n_mels=64)
D2 = librosa.power_to_db(S2, ref=np.max)
plot5 = plt.subplot(5,1,5)
librosa.display.specshow(D2, x_axis='time', y_axis='mel')
plt.show()