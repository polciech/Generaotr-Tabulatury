import sys
import threading
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QPushButton, QMainWindow, QLabel, QFileDialog, QSizePolicy, QFileDialog, QSizePolicy, QVBoxLayout, QWidget, QComboBox, QHBoxLayout
from PySide6.QtGui import QFont
from PySide6.QtCore import QFile, QFileSystemWatcher, QFile, QFileSystemWatcher, Slot
from PySide6.QtGui import QBrush, QColor, QLinearGradient, QPainter, QPalette, QCursor
from PySide6.QtGui import QIcon
import pyaudio
import wave
import os
from testowy import find_notes, creating_tab, writing_to_txt_file

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
input_id = 0
record_button_state = False
class GUI(QMainWindow):
    def __init__(self):
        super(GUI, self).__init__()
        self.setGeometry(0, 0, 1920, 1080)
        self.setWindowTitle("Generator Tabulatury")
        self.initUI()
        
        self.isrecording = False


    def initUI(self):
        self.label = QLabel(self)
        self.label.setText("kliknij guzik aby zaczac nagrywanie")
        self.label.move(50, 50)
        self.tab = QLabel(self)
        self.state = 0
        self.pane = QLabel()
        self.pane.setStyleSheet('background-color: #181818;')
        self.pane.setGeometry(0,0,1920,100)
        self.line = QLabel()
        self.line.setStyleSheet('background-color: #282828;')
        self.line.setGeometry(0,100,1920,2)
        self.gradient = QLabel()
        self.gradient.setGeometry(0,102,1920,978)
        self.record_button = QPushButton(QIcon("microphone_unhovered.png"), "", self)
        self.record_button.setIconSize(self.record_button.size())
        self.play_button = QPushButton(QIcon("play.png"), "", self)
        self.play_button.setIconSize(self.play_button.size())
        self.change_button = QPushButton(QIcon("plus.png"), "", self)
        self.change_button.setIconSize(self.change_button.size())
        self.load_button = QPushButton(QIcon("save.png"), "", self)
        self.load_button.setIconSize(self.load_button.size())
        self.record_button.clicked.connect(self.click)
        # self.record_button.move(110, 130)
        # self.record_button.setFixedSize(120, 60)
        # self.play_button.setFixedSize(120, 60)
        # self.change_button.setFixedSize(120, 60)
        self.record_button.setMouseTracking(True)
        self.record_button.enterEvent = lambda event: self.record_button.setIcon(QIcon('microphone_hovered.png'))
        self.record_button.leaveEvent = lambda event: self.record_button.setIcon(QIcon('microphone_unhovered.png'))

        self.load_button.setMouseTracking(True)
        self.load_button.enterEvent = lambda event: self.load_button.setIcon(QIcon('save.png'))
        self.load_button.leaveEvent = lambda event: self.load_button.setIcon(QIcon('save_unhovered.png'))

        self.tab.setText("Loading file...")
        self.tab.move(110, 170)

        button_style = """
                    QPushButton {background-color: transparent; border-radius: 5px; border-style: none; color: white; height: 50px;
                    width: 50px;
                }
            """
        # Set cursor shape on hover
        self.record_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.play_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.change_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.load_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.record_button.setStyleSheet(button_style)
        self.play_button.setStyleSheet(button_style)
        self.change_button.setStyleSheet(button_style)
        self.load_button.setStyleSheet(button_style)

        # Set background color and gradient
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor('#181818'))
        gradient.setColorAt(1, QColor(84, 24, 60))
        self.gradient.setAutoFillBackground(True)
        p = self.palette()
        p.setBrush(QPalette.Window, QBrush(gradient))
        self.gradient.setPalette(p)

        # Create a QFont instance for Consolas font
        consolas_font = QFont("Consolas", 12)

        # Set the font for the QLabel widget
        self.tab.setFont(consolas_font)

        self.record_button.clicked.connect(self.on_file_changed)
        self.filepath = "tab.txt"
        self.file = QFile("tab.txt")
        self.file.open(QFile.ReadOnly | QFile.Text)
        
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
        self.dropdown.setFixedWidth(200)

        # Connect the dropdown's signal to a slot that updates the label
        self.dropdown.currentTextChanged.connect(self.update_list)

        # Set the label to resize automatically
        self.tab.setWordWrap(True)
        self.tab.setScaledContents(True)
        self.tab.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Set a minimum width for the label (optional)
        self.tab.setMinimumHeight(170)

        # Create a vertical layout and add the label to it
        tab_layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        label_layout = QVBoxLayout()
        line_layout = QHBoxLayout()
        label_layout.addWidget(self.label)
        button_layout.addWidget(self.record_button)
        button_layout.addWidget(self.play_button)
        button_layout.addWidget(self.change_button)
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.dropdown)
        button_layout.setContentsMargins(500, 0, 500, 0)
        button_layout.setMenuBar(self.pane)
        line_layout.setMenuBar(self.line)
        tab_layout.setMenuBar(self.gradient)
        # button_layout.addWidget(self.list)
        tab_layout.addWidget(self.tab)

        # Add the button layout and widget layout to a main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(label_layout)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(line_layout)
        main_layout.addLayout(tab_layout)

        # Create a central widget and set the layout as its layout
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

        # Set the main window's size policy to expanding in both directions
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.watcher = QFileSystemWatcher()
        self.watcher.addPath("tab.txt")
        self.watcher.fileChanged.connect(self.on_file_changed)

    @Slot(str)
    def on_file_changed(self, path):
        if path == self.filepath:
            self.file.seek(0)
            self.tab.setText(self.file.readAll().data().decode('utf-8'))

    def click(self):
        self.update()
        if self.isrecording:
            self.isrecording = False

        else:
            self.isrecording = True
            self.label.setText("nagrywanie...")
            threading.Thread(target=self.record).start()

    def update_list(self):
        self.dropdown.setText(self.dropdown.currentText())
        self.input_id = self.dropdown.currentIndex()-1

    def record(self):
            
        audio = pyaudio.PyAudio()
        stream = audio.open(format= FORMAT, channels=CHANNELS,rate= RATE, frames_per_buffer= CHUNK,input= True, input_device_index=input_id)

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
        writing_to_txt_file(creating_tab(find_notes(f"recording{i}.wav")))

    def update(self):
        self.label.adjustSize()

def window ():
    app = QApplication(sys.argv)
    win = GUI()
    win.show()
    sys.exit(app.exec())

window()
