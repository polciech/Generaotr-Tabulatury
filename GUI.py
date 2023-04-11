import sys
import threading
from PySide6.QtWidgets import QApplication, QPushButton, QMainWindow, QLabel
from PySide6.QtCore import Slot
import pyaudio
import wave
import os
from testowy import find_notes, creating_tab, writing_to_txt_file

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100


class GUI(QMainWindow):
    def __init__(self):
        super(GUI, self).__init__()
        self.setGeometry(300, 200, 300, 300)
        self.setWindowTitle("Generator Tabulatury")
        self.initUI()
        self.isrecording = False


    def initUI(self):
        self.label = QLabel(self)
        self.label.setText("kliknij guzik aby zaczac nagrywanie")
        self.label.move(50, 50)

        self.state = 0
        self.b1 = QPushButton(self)
        self.b1.clicked.connect(self.click)
        self.b1.setText("rozpocznij nagrywanie")
        self.b1.move(110, 130)

    def click(self):
        self.update()
        if self.isrecording:
            self.isrecording = False

        else:
            self.isrecording = True
            self.label.setText("nagrywanie...")
            threading.Thread(target=self.record).start()

    def record(self):
            audio = pyaudio.PyAudio()
            stream = audio.open(format= FORMAT, channels=CHANNELS,rate= RATE, frames_per_buffer= CHUNK,input= True)

            print('starting recording')

            frames = []


            while self.isrecording:
                data = stream.read(CHUNK)
                frames.append(data)

            sample_width = audio.get_sample_size(FORMAT)

            #zamykanie sesji nagrywania
            stream.stop_stream()
            stream.close()
            audio.terminate()

            exists = True
            i = 1

            while exists :
                if os.path.exists(f"recording{i}.wav"):
                    i += 1
                else:
                    exists = False

            wf = wave.open(f"recording{i}.wav", 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(sample_width)
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()
            print(f"zapisano recording numer {i}")
            writing_to_txt_file(creating_tab(find_notes(f"recording{i}.wav")))



    def update(self):
        self.label.adjustSize()




def window ():
    app = QApplication(sys.argv)
    win = GUI()
    win.show()
    sys.exit(app.exec())

window()
