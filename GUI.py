import sys, threading, pyaudio, wave, os
from PySide6.QtCore import Qt, QFile, QFileSystemWatcher, QFile, QFileSystemWatcher, Slot
from PySide6.QtWidgets import QApplication, QPushButton, QMainWindow, QLabel, QFileDialog, QSizePolicy, QFileDialog, QSizePolicy, QVBoxLayout, QWidget, QComboBox, QHBoxLayout, QScrollArea, QScrollBar, QAbstractScrollArea
from PySide6.QtGui import QBrush, QColor, QLinearGradient, QPalette, QCursor, QIcon, QFont, QPainter
from testowy import find_notes, creating_tab, writing_to_txt_file
import numpy as np
import sounddevice as sd
import soundfile as sf
import time
import rt_process
from buffer import AudioBuffer
import crepe
from scipy.io import wavfile
import math
import librosa

wybrane_strojenie = 0
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
input_id = 0
record_button_state = False
class GUI(QMainWindow):
    def __init__(self):
        super(GUI, self).__init__()
        self.setWindowTitle("GENERATOR TABULATURY")
        self.initUI()
        
        # Set the window flags to enable custom title bar
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setGeometry(0,0,1920,1080)
        self.showMaximized()
        self.isrecording = False
        self.isplaying = False
        self.PLAY_ICON = 'play.png'
        self.PLAY_ICON_UNHOVERED = 'play_unhovered.png'
        self.REC = 'microphone_hovered.png'
        self.REC_UNHOVERED = 'microphone_unhovered.png'
        self.input_id = 0
    def initUI(self):
    
    #Titlebar: title, minimize, maximize, close

        self.title = QLabel("Generator Tabulatury")
        self.title.setStyleSheet('background-color: transparent; border-style: none; color: white;')

        # Create a QFont instance for Consolas font
        title_font = QFont("Bahnschrift", 16)

        # Set the font for the QLabel widget
        self.title.setFont(title_font)

        self.close_button = QPushButton(QIcon("close.png"), "", self)
        self.minimize = QPushButton(QIcon("minimize.png"), "", self)
        self.maximize = QPushButton(QIcon("maximize.png"), "", self)
        self.close_button.setIconSize(self.close_button.size())
        self.minimize.setIconSize(self.minimize.size())
        self.maximize.setIconSize(self.maximize.size())
        self.close_button.setFixedSize(40,25)
        self.minimize.setFixedSize(40,25)
        self.maximize.setFixedSize(40,25)
        
        self.close_button.clicked.connect(self.close_everything)
        self.minimize.clicked.connect(self.showMinimized)
        self.maximize.clicked.connect(self.minmax)

        close_style = """
            QPushButton {
                background-color: transparent; border-style: none;
            }
            QPushButton:hover {
                background-color: #ff2e2e; border-style: none;
            }
            """
        
        minmax_style = """
            QPushButton {
                background-color: transparent; border-style: none;
            }
            QPushButton:hover {
                background-color: #474747; border-style: none;
            }
            """
    
        self.close_button.setStyleSheet(close_style)
        self.minimize.setStyleSheet(minmax_style)
        self.maximize.setStyleSheet(minmax_style)



    #Main menu; buttons, list

        #Style sheets for buttons


        button_style = """
                    QPushButton {background-color: transparent; border-radius: 0px; border-style: none; color: white; height: 50px;
                    width: 50px;
                }
            """
        record_button_style = """
                    QPushButton {background-color: transparent; border-radius: 0px; border-style: none; color: white; height: 50px;
                    width: 50px;
                }
            """


        self.close_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.minimize.setCursor(QCursor(Qt.PointingHandCursor))
        self.maximize.setCursor(QCursor(Qt.PointingHandCursor))

        self.tab = QLabel(self)
        self.tab.setStyleSheet('background-color: transparent; color: white;')
        self.state = 0
        self.pane = QLabel()
        self.pane.setStyleSheet('background-color: #181818;')
        self.pane.setGeometry(0,0,1920,100)
        self.line = QLabel()
        self.line.setStyleSheet('background-color: #282828;')
        self.line.setGeometry(0,100,1920,2)
        self.gradient = QLabel()
        self.gradient.setGeometry(0,102,1920,978)
        self.tab.setGeometry(0,102,1920,978)
        self.record_button = QPushButton(QIcon("microphone_unhovered.png"), "", self)
        self.record_button.setIconSize(self.record_button.size())
        self.play_button = QPushButton(QIcon("play_unhovered.png"), "", self)
        self.play_button.setIconSize(self.play_button.size())
        self.change_button = QPushButton(QIcon("plus_unhovered.png"), "", self)
        self.change_button.setIconSize(self.change_button.size())
        self.load_button = QPushButton(QIcon("load_unhovered.png"), "", self)
        self.load_button.setIconSize(self.load_button.size())

        self.record_button.clicked.connect(self.click)

        self.record_button.setMaximumWidth(50)
        self.play_button.setMaximumWidth(50)
        self.load_button.setMaximumWidth(50)
        self.change_button.setMaximumWidth(50)

        self.record_button.setMouseTracking(True)
        self.record_button.enterEvent = lambda event: self.record_button.setIcon(QIcon(self.REC))
        self.record_button.leaveEvent = lambda event: self.record_button.setIcon(QIcon(self.REC_UNHOVERED))

        self.load_button.setMouseTracking(True)
        self.load_button.enterEvent = lambda event: self.load_button.setIcon(QIcon('load.png'))
        self.load_button.leaveEvent = lambda event: self.load_button.setIcon(QIcon('load_unhovered.png'))

        self.change_button.setMouseTracking(True)
        self.change_button.enterEvent = lambda event: self.change_button.setIcon(QIcon(self.PLAY_ICON))
        self.change_button.leaveEvent = lambda event: self.change_button.setIcon(QIcon(self.PLAY_ICON_UNHOVERED))

        self.play_button.setMouseTracking(True)
        self.play_button.enterEvent = lambda event: self.play_button.setIcon(QIcon(self.PLAY_ICON))
        self.play_button.leaveEvent = lambda event: self.play_button.setIcon(QIcon(self.PLAY_ICON_UNHOVERED))

        # Create a dropdown list
        self.dropdown = QComboBox(self)

        audio = pyaudio.PyAudio()
        info = audio.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')

        self.dropdown.addItem('Wybierz wejście mikrofonowe')
        for i in range(0, numdevices):
            if (audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                self.dropdown.addItem(audio.get_device_info_by_host_api_device_index(0, i).get('name'))
        

        self.dropdown.setStyleSheet("background-color: #464646; border-radius: 5px; border-style: none; color: white;")
        self.dropdown.setFixedWidth(175)

        self.strojenia = QComboBox(self)

        strojenia = ['Standardowy strój', 'Drop D', 'DADGAD', 'Double Drop D', 'D7sus4', 'Open D Major', 'Cmaj9sus4', 'Cmaj7sus4', 'Csus4', 'Open A Major', 'Open E Major', 'E Minor Sus4', 'Double E Double A', 'Open G Major']

        for i in range(0, len(strojenia)):
            self.strojenia.addItem(strojenia[i], userData=i)

        self.strojenia.setStyleSheet("background-color: #464646; border-radius: 5px; border-style: none; color: white;")
        self.strojenia.setFixedWidth(175)
        self.strojenia.currentIndexChanged.connect(self.handle_selection_change)

        # Connect the dropdown's signal to a slot that updates the label
        self.dropdown.currentTextChanged.connect(self.update_list)

        self.tab.setText("Nagraj dźwięk lub otwórz poprzednie nagranie...")
        self.tab.move(110, 170)

        # Set cursor shape on hover
        self.record_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.play_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.change_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.load_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.record_button.setStyleSheet(record_button_style)
        self.play_button.setStyleSheet(button_style)
        self.change_button.setStyleSheet(button_style)
        self.load_button.setStyleSheet(button_style)
        self.play_button.clicked.connect(self.play_sound)
        self.load_button.clicked.connect(self.load)

    #Tabulature window

        # Set background color and gradient
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor('#181818'))
        gradient.setColorAt(1, QColor('#54183c'))
        self.gradient.setAutoFillBackground(True)
        p = self.palette()
        p.setBrush(QPalette.Window, QBrush(gradient))
        self.gradient.setPalette(p)

        # Create a QFont instance for Consolas font
        consolas_font = QFont("Consolas", 16)

        # Set the font for the QLabel widget
        self.tab.setFont(consolas_font)

        self.record_button.clicked.connect(self.on_file_changed)
        self.filepath = "tab.txt"
        self.file = QFile("tab.txt")
        self.file.open(QFile.ReadOnly | QFile.Text)

        # Set the label to resize automatically
        self.tab.setWordWrap(True)
        self.tab.setScaledContents(True)
        

        self.scrollTab = QScrollArea()
        self.scrollTab.setWidget(self.tab)
        self.scrollTab.setWidgetResizable(True)
        self.scrollTab.setStyleSheet("background-color: transparent; border: none;")
        self.scrollTab.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollTab.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    #Layouts

        # Create a vertical layout and add the label to it
        widget = QWidget()
        title_layout = QHBoxLayout()
        title_buttons_layout = QHBoxLayout()
        title_bar_layout = QHBoxLayout()
        tab_layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        
        title_layout.addWidget(self.title)
        title_layout.setSpacing(0)
        title_layout.setAlignment(Qt.AlignLeft)

        title_buttons_layout.addWidget(self.minimize)
        title_buttons_layout.addWidget(self.maximize)
        title_buttons_layout.addWidget(self.close_button)
        title_buttons_layout.setSpacing(0)
        title_buttons_layout.setAlignment(Qt.AlignRight)
        
        title_bar_layout.addLayout(title_layout)
        title_bar_layout.addLayout(title_buttons_layout)
        title_bar_layout.setMenuBar(self.pane)
        button_layout.addWidget(self.strojenia)
        button_layout.addWidget(self.play_button)
        button_layout.addWidget(self.record_button)
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.dropdown)
        button_layout.setSpacing(0)
        button_layout.setAlignment(Qt.AlignCenter)
        

        button_layout.setMenuBar(self.line)
        tab_layout.setMenuBar(self.gradient)
        # button_layout.addWidget(self.list)
        tab_layout.addWidget(self.scrollTab)
        tab_layout.setAlignment(Qt.AlignCenter)

        # Add the button layout and widget layout to a main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(title_bar_layout)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(tab_layout)
        

        # Create a central widget and set the layout as its layout
        
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

        # Set the main window's size policy to expanding in both directions
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.watcher = QFileSystemWatcher()
        self.watcher.addPath("tab.txt")
        self.watcher.fileChanged.connect(self.on_file_changed)
        



    @Slot(str)
    def close_everything(self):
        self.isrecording=False
        self.close()

    def on_file_changed(self, path):
        if path == self.filepath:
            self.file.seek(0)
            self.tab.setText(self.file.readAll().data().decode('utf-8'))
            # self.scrollTab.horizontalScrollBar().setValue(self.scrollTab.horizontalScrollBar().maximum())

    def click(self):
        if self.isrecording:
            self.isrecording = False
            self.REC = 'microphone_hovered.png'
            self.REC_UNHOVERED = 'microphone_unhovered.png'
        else:
            self.isrecording = True
            threading.Thread(target=self.record).start()
            self.REC = 'microphone_record.png'
            self.REC_UNHOVERED = 'microphone_record_unhovered.png'


    def update_list(self):
        self.input_id = self.dropdown.currentIndex()-1

    def minmax(self):
        if self.isMaximized():
            self.showFullScreen()
        elif self.isFullScreen():
            self.showMaximized()

    def load(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Load File", "", "Txt Files (data*.txt)", options=options)
        if fileName:
            print("Selected file:", fileName)

        self.final_notes = []
        self.final_freqs = []

        with open(fileName, 'r') as file:
            lines = file.readlines()
            if len(lines) >= 1:
                self.final_notes.extend((lines[0].strip()).split())
            if len(lines) >= 2:
                self.final_freqs.extend((lines[1].strip()).split())
            writing_to_txt_file(creating_tab(self.final_notes, wybrane_strojenie))

        self.play()

    def handle_selection_change(self, index):
        wybrane_strojenie = self.strojenia.currentData()
        print(wybrane_strojenie)
        writing_to_txt_file(creating_tab(self.final_notes, wybrane_strojenie))

    def record(self):
        # audio = pyaudio.PyAudio()
        # stream = audio.open(format= FORMAT, channels=CHANNELS,rate= RATE, frames_per_buffer= CHUNK,input= True)
        # print('starting recording')

        # frames = []


        # while self.isrecording:
        #     data = stream.read(CHUNK)
        #     frames.append(data)

        # sample_width = audio.get_sample_size(FORMAT)

        # #zamykanie sesji nagrywania
        # stream.stop_stream()
        # stream.close()
        # audio.terminate()

        # exists = True
        # i = 1

        # while exists :
        #     if os.path.exists(f"recording{i}.wav"):
        #         i += 1
        #     else:
        #         exists = False

        # wf = wave.open(f"recording{i}.wav", 'wb')
        # wf.setnchannels(CHANNELS)
        # wf.setsampwidth(sample_width)
        # wf.setframerate(RATE)
        # wf.writeframes(b''.join(frames))
        # wf.close()

        # self.final_notes, self.final_freqs = find_notes(f"recording{i}.wav")

        audio = pyaudio.PyAudio()
        stream = audio.open(format= FORMAT, channels=CHANNELS,rate= RATE, frames_per_buffer= CHUNK,input= True, input_device_index=input_id)

        frames = []

        audio_buffer = AudioBuffer()
        audio_buffer.start()
        audio_buffer.setInput_id(self.input_id)
        self.final_notes =[]
        self.final_freqs = []
        previous_note = None

        while self.isrecording:
            audio_data = audio_buffer()
            note, freq= rt_process.find_notes(audio_data)
            f_size = len(note)
            for i in range(f_size):
                if note[i] != previous_note:
                    self.final_freqs.append(freq[i])
                    self.final_notes.append(note[i])
                    previous_note = note[i]
                    writing_to_txt_file(creating_tab(self.final_notes, wybrane_strojenie))
        print(self.final_notes)
        audio_buffer.stop()
        
        # exists = True
        # i = 1
        # while exists :
        #     if os.path.exists(f"data{i}.txt"):
        #         i += 1
        #     else:
        #         exists = False

        # with open(f"data{i}.txt", 'w') as file:
        #     if self.final_notes:
        #         for i in self.final_notes:
        #             file.write(str(i) + ' ')
        #         file.write('\n')
        #     if self.final_freqs:
        #         for i in self.final_freqs:
        #             file.write(str(i) + ' ')

        
        exists = True
        i = 1
        while exists :
            if os.path.exists(f"tab{i}.txt"):
                i += 1
            else:
                exists = False

        with open("tab.txt", 'w') as tab:
            tab.write(creating_tab(self.final_notes, wybrane_strojenie))

        with open(f"tab{i}.txt", 'w') as file_tab:
            file_tab.write(creating_tab(self.final_notes, wybrane_strojenie))


        # self.play()

    def play(self):
        
        # Set the sample rate and duration
        sample_rate = 44100 # in Hz
        duration = 0.3 # in seconds

        # Define a function to generate a sawtooth wave for a given frequency
        def generate_sawtooth_wave(frequency, duration, sample_rate):
            # Calculate the number of samples
            num_samples = duration * sample_rate

            # Calculate the time array
            time_array = np.arange(num_samples) / sample_rate

            # Calculate the sawtooth wave
            sawtooth_wave = 2 * (frequency * time_array - np.floor(0.5 + frequency * time_array))

            # Normalize the waveform
            sawtooth_wave /= np.max(np.abs(sawtooth_wave))

            return sawtooth_wave

        # Define a function to generate a square wave for a given frequency
        def generate_square_wave(frequency, duration, sample_rate):
            # Calculate the number of samples
            num_samples = duration * sample_rate

            # Calculate the time array
            time_array = np.arange(num_samples) / sample_rate

            # Calculate the square wave
            square_wave = np.sign(np.sin(2 * np.pi * frequency * time_array))

            # Normalize the waveform
            square_wave /= np.max(np.abs(square_wave))

            return square_wave

        # Define a function to generate a sine wave for a given frequency
        def generate_sine_wave(frequency, duration, sample_rate):
            # Calculate the number of samples
            num_samples = duration * sample_rate

            # Calculate the time array
            time_array = np.arange(num_samples) / sample_rate

            # Calculate the sine wave
            sine_wave = np.sin(2 * np.pi * frequency * time_array)

            # Normalize the waveform
            sine_wave /= np.max(np.abs(sine_wave))

            return sine_wave

        sound = np.array([])
        # Generate the sawtooth, square, and sine waves for a given note
        for frequency in self.final_freqs:
            sawtooth_wave = generate_sawtooth_wave(float(frequency), duration, sample_rate)
            square_wave = generate_square_wave(float(frequency), duration, sample_rate)
            sine_wave = generate_sine_wave(float(frequency), duration, sample_rate)
            combined_wave = sawtooth_wave + sine_wave
            sound = np.concatenate((sound, combined_wave))
        
        output_play = "play.wav"
        sf.write(output_play, sound, sample_rate)

    def play_sound(self):
        if self.isplaying:
            self.isplaying = False
            sd.stop()
            self.PLAY_ICON = 'play.png'
            self.PLAY_ICON_UNHOVERED = 'play_unhovered.png'
            
        else:
            self.isplaying = True
            audio_data, _ = sf.read("play.wav")
            sd.play(audio_data, 44100)
            self.PLAY_ICON = 'stop.png'
            self.PLAY_ICON_UNHOVERED = 'stop_unhovered.png'
            

def window ():
    app = QApplication(sys.argv)
    win = GUI()
    win.show()
    sys.exit(app.exec())

window()





