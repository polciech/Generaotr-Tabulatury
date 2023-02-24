import pyaudio
import wave

#paramtetry nagrania
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

def record():

	#inicjowanie sesji audio
	audio = pyaudio.PyAudio()

	stream = audio.open(format= FORMAT, channels=CHANNELS,rate= RATE, frames_per_buffer= CHUNK,input= True)

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


