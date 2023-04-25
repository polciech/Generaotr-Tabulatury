# import sys
# from PySide6.QtCore import QTimer
# from PySide6.QtGui import QPalette, QColor
# from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         self.setWindowTitle("Button Click Example")
#         self.setGeometry(100, 100, 400, 300)

#         self.button = QPushButton("Click Me", self)
#         self.button.setGeometry(150, 100, 100, 50)
#         self.button.clicked.connect(self.on_button_click)

#     def on_button_click(self):
#         self.button.setStyleSheet("background-color: violet")
#         QTimer.singleShot(75, self.reset_button_color)

#     def reset_button_color(self):
#         self.button.setStyleSheet("")
#         self.button.setAutoFillBackground(False)
#         pal = QPalette()
#         self.button.setPalette(pal)

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     main_window = MainWindow()
#     main_window.show()
#     sys.exit(app.exec_())


# ===================================================================================================================================




# import sys
# from PySide6.QtCore import Qt
# from PySide6.QtGui import QBrush, QColor, QLinearGradient, QPainter, QPalette
# from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QListWidget, QAbstractItemView, QHBoxLayout, QVBoxLayout, QWidget


# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("PySide6 GUI Example")

#         # Set background color and gradient
#         gradient = QLinearGradient(0, 0, 0, self.height())
#         gradient.setColorAt(0, QColor(45, 43, 59))
#         gradient.setColorAt(1, QColor(109, 33, 79))
#         self.setAutoFillBackground(True)
#         p = self.palette()
#         p.setBrush(QPalette.Window, QBrush(gradient))
#         self.setPalette(p)

#         # Create a horizontal layout for the buttons
#         button_layout = QHBoxLayout()

#         # Create a display label
#         display_label = QLabel(self)
#         display_label.setGeometry(50, 50, 200, 30)
#         display_label.setStyleSheet("background-color: #8a668b; border-radius: 5px; border-style: none; color: white;")

#         # Create a button to set display text
#         set_text_button = QPushButton("Set Text", self)
#         set_text_button.setStyleSheet("background-color: #e09ee8; border-radius: 5px; border-style: none; color: white;")
#         set_text_button.clicked.connect(lambda: display_label.setText("Display Text"))

#         # Create a button to clear display text
#         clear_text_button = QPushButton("Clear Text", self)
#         clear_text_button.setStyleSheet("background-color: #e09ee8; border-radius: 5px; border-style: none; color: white;")
#         clear_text_button.clicked.connect(lambda: display_label.setText(""))

#         # Create a button to exit the application
#         exit_button = QPushButton("Exit", self)
#         exit_button.setStyleSheet("background-color: #e09ee8; border-radius: 5px; border-style: none; color: white;")
#         exit_button.clicked.connect(self.close)

#         # Add the buttons to the layout
#         button_layout.addWidget(set_text_button)
#         button_layout.addWidget(clear_text_button)
#         button_layout.addWidget(exit_button)

#         # Make the buttons tighter but higher
#         set_text_button.setFixedSize(120, 60)
#         clear_text_button.setFixedSize(120, 60)
#         exit_button.setFixedSize(120, 60)

#         # Create a vertical layout for the widgets
#         widget_layout = QVBoxLayout()
#         widget_layout.addWidget(display_label)

#         # Create a scrollable list
#         list_widget = QListWidget(self)
#         list_widget.setStyleSheet("""
#             background-color: #56475e;
#             border-radius: 5px;
#             border-style: none;
#             color: white;
#             selection-color: black;
#             selection-background-color: #8a668b;
#             """)

#         # Add items to the list widget
#         for i in range(20):
#             list_widget.addItem(f"Item {i+1}")

#         # Set list widget selection mode to multi selection
#         list_widget.setSelectionMode(QAbstractItemView.MultiSelection)

#         # Add the list widget to the layout
#         widget_layout.addWidget(list_widget)

#         # Make the list widget a bit darker
#         p = list_widget.palette()
#         p.setColor(QPalette.Base, QColor(86, 71, 94))
#         p.setColor(QPalette.Text, Qt.white)
#         list_widget.setPalette(p)

#         # Add the button layout and widget layout to a main layout
#         main_layout = QVBoxLayout()
#         main_layout.addLayout(button_layout)
#         main_layout.addLayout(widget_layout)

#         # Create a widget to hold the main layout
#         widget = QWidget()
#         widget.setLayout(main_layout)

#         # Set the central widget of the main window to the widget
#         self.setCentralWidget(widget)

#         # Set the window size to Full HD resolution and show the window
#         self.setGeometry(0, 0, 1920, 1080)
#         self.show()

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.setGeometry(100, 100, 300, 400)
#     window.show()
#     sys.exit(app.exec())


# ===================================================================================================================================


# import sys
# from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
# from PySide6.QtGui import QIcon

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("PySide6 GUI Example")

#         # Create a button with microphone icon
#         microphone_button = QPushButton(QIcon("microphone.png"), "", self)
#         microphone_button.setIconSize(microphone_button.size()) # set the icon size to the size of the button
#         microphone_button.resize(80, 80) # resize the button to make it visible

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec())


# import sys
# from PySide6.QtWidgets import QApplication, QComboBox, QLabel, QMainWindow

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         # Create a dropdown list
#         self.dropdown = QComboBox(self)
#         self.dropdown.addItems(['Option 1', 'Option 2', 'Option 3'])
#         self.dropdown.setGeometry(50, 50, 100, 25)

#         # Add a label to display the selected option
#         self.label = QLabel(self)
#         self.label.setGeometry(50, 100, 100, 25)
#         self.label.setText('Selected option:')

#         # Connect the dropdown's signal to a slot that updates the label
#         self.dropdown.currentTextChanged.connect(self.update_label)

#     def update_label(self):
#         self.label.setText('Selected option: ' + self.dropdown.currentText())

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())

# =======================================================================================================================

# import sys
# from PySide6.QtCore import Qt
# from PySide6.QtGui import QFont, QCursor
# from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton


# class Example(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         self.initUI()

#     def initUI(self):
#         self.button = QPushButton('Button', self)
#         self.button.setGeometry(50, 50, 100, 50)

#         # Set button font
#         font = QFont()
#         font.setPointSize(12)
#         self.button.setFont(font)

#         # Set cursor shape on hover
#         self.button.setCursor(QCursor(Qt.PointingHandCursor))

#         # Set button stylesheet
#         button_style = """
#             QPushButton {
#                 background-color: #3daee9;
#                 border: none;
#                 color: white;
#                 border-radius: 10px;
#             }
#             QPushButton:hover {
#                 background-color: #4fb7ff;
#                 font-size: 14px;
#                 height: 60px;
#                 width: 120px;
#             }
#         """
#         self.button.setStyleSheet(button_style)

#         self.setGeometry(300, 300, 200, 150)
#         self.setWindowTitle('Example')

#         self.show()


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = Example()
#     sys.exit(app.exec())

#======================================================================================================

# import sys
# from PySide6.QtCore import Qt, QRect, QPoint
# from PySide6.QtGui import QColor, QPainter, QBrush
# from PySide6.QtWidgets import QApplication, QMainWindow, QSlider

# class SpotifySlider(QSlider):
#     def __init__(self, orientation):
#         super().__init__(orientation)
#         self.setStyleSheet("""
#             QSlider::groove:horizontal {
#                 border: 1px solid #bbb;
#                 background: white;
#                 height: 10px;
#                 border-radius: 5px;
#             }
            
#             QSlider::sub-page:horizontal {
#                 background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #7CB342, stop:1 #7CB342);
#                 border: 1px solid #777;
#                 height: 10px;
#                 border-radius: 5px;
#             }
            
#             QSlider::add-page:horizontal {
#                 background: #eee;
#                 border: 1px solid #777;
#                 height: 10px;
#                 border-radius: 5px;
#             }
            
#             QSlider::handle:horizontal {
#                 background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #F5F5F5, stop:1 #F1F1F1);
#                 border: 1px solid #777;
#                 width: 20px;
#                 margin: -5px 0;
#                 border-radius: 10px;
#             }
#         """)
    
#     def paintEvent(self, event):
#         # Override the paintEvent method to draw a circle around the handle
#         super().paintEvent(event)
#         painter = QPainter(self)
#         painter.setRenderHint(QPainter.Antialiasing)
#         handle_center = QPoint(self.width() * self.value() / self.maximum(), self.height() / 2)
#         handle_radius = 12
#         brush = QBrush(QColor("#7CB342"))
#         painter.setBrush(brush)
#         painter.setPen(Qt.NoPen)
#         painter.drawEllipse(QRect(handle_center - QPoint(handle_radius, handle_radius), handle_center + QPoint(handle_radius, handle_radius)))

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Slider Example")

#         # Create a Spotify-style slider widget and set its properties
#         self.slider = SpotifySlider(Qt.Horizontal)
#         self.slider.setMinimum(0)
#         self.slider.setMaximum(100)
#         self.slider.setValue(50)
#         self.slider.setTickPosition(QSlider.NoTicks)

#         # Add the slider widget to the main window
#         self.setCentralWidget(self.slider)

#     def slider_changed(self, value):
#         # This function will be called whenever the slider's value changes
#         print(f"Slider value changed: {value}")

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec())

#========================================================================================================================

# import sys
# from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QPushButton, QVBoxLayout, QSizePolicy

# class MyWidget(QWidget):
#     def __init__(self):
#         super().__init__()

#         # create a horizontal layout for the buttons
#         hbox = QHBoxLayout()

#         # create the three buttons
#         previous_button = QPushButton('Previous')
#         play_button = QPushButton('Play')
#         next_button = QPushButton('Next')

#         # add some padding between the buttons
#         hbox.setSpacing(10)

#         # add the buttons to the layout with stretch factors
#         hbox.addWidget(previous_button, 1)
#         hbox.addWidget(play_button, 2)
#         hbox.addWidget(next_button, 1)

#         # create a vertical layout for the widget
#         vbox = QVBoxLayout()
#         vbox.addStretch()
#         vbox.addLayout(hbox)
#         vbox.addStretch()
#         vbox.setContentsMargins(400, 0, 400, 0)

#         # set the layout for the widget
#         self.setLayout(vbox)

#         # set the size of the widget to half of the screen size
#         screen = QApplication.primaryScreen()
#         screen_size = screen.availableGeometry()
#         self.setGeometry(0,0,1920,1080)

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     widget = MyWidget()
#     widget.show()
#     sys.exit(app.exec())

# ============================================================================



# import sys
# from PySide6.QtCore import Qt
# from PySide6.QtGui import QColor
# from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton

# class MyWindow(QWidget):
#     def __init__(self):
#         super().__init__()

#         # Set the window flags to enable custom title bar
#         self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)

#         # Set the background color to transparent
#         self.setAttribute(Qt.WA_TranslucentBackground)

#         # Create the UI elements
#         title_bar = self.create_title_bar()

#         label = QLabel("Hello World!")
#         layout = QVBoxLayout()
#         layout.addWidget(title_bar)
#         layout.addWidget(label)
#         self.setLayout(layout)

#     def create_title_bar(self):
#         # Create the UI elements for the custom title bar
#         minimize_button = QPushButton("Minimize")
#         maximize_button = QPushButton("Maximize")
#         close_button = QPushButton("Close")

#         # Set the layout of the custom title bar
#         layout = QHBoxLayout()
#         layout.addWidget(minimize_button)
#         layout.addWidget(maximize_button)
#         layout.addWidget(close_button)
#         layout.setAlignment(Qt.AlignRight)
#         layout.setSpacing(0)
#         layout.setContentsMargins(0, 0, 0, 0)

#         # Create the widget for the custom title bar and set its layout
#         title_bar_widget = QWidget()
#         title_bar_widget.setLayout(layout)
#         title_bar_widget.setStyleSheet("background-color: #282828;")

#         return title_bar_widget

# app = QApplication(sys.argv)

# window = MyWindow()
# window.setGeometry(100, 100, 400, 300)
# window.show()

# sys.exit(app.exec())

# ========================================================================================================================================

# import sys
# from PySide6.QtCore import Qt, QPoint
# from PySide6.QtGui import QCursor
# from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout

# class MyWindow(QWidget):
#     def __init__(self):
#         super().__init__()

#         # Set window properties
#         self.setWindowFlags(Qt.FramelessWindowHint)

#         # Create UI elements
#         title_bar = QLabel("My Window Title")
#         content = QLabel("Window Content")
#         button_layout = QHBoxLayout()
#         button_layout.addStretch()
#         button_layout.addWidget(QLabel("Button 1"))
#         button_layout.addWidget(QLabel("Button 2"))
#         button_layout.addWidget(QLabel("Button 3"))

#         # Create layout
#         layout = QVBoxLayout()
#         layout.addWidget(title_bar)
#         layout.addWidget(content)
#         layout.addLayout(button_layout)
#         self.setLayout(layout)

#         # Store the initial click position and whether the cursor is in the button layout
#         self.click_position = None
#         self.cursor_in_buttons = False

#     def mousePressEvent(self, event):
#         if event.button() == Qt.LeftButton:
#             # Check if the cursor is in the button layout
#             cursor_pos = event.pos()
#             button_layout_pos = self.layout().itemAt(2).geometry()
#             if button_layout_pos.contains(cursor_pos):
#                 self.cursor_in_buttons = True
#                 # Store the click position relative to the window
#                 self.click_position = QCursor.pos() - self.frameGeometry().topLeft()
#                 event.accept()

#     def mouseMoveEvent(self, event):
#         if event.buttons() == Qt.LeftButton and self.click_position is not None and self.cursor_in_buttons:
#             # Move the window by the distance the mouse has been dragged since the click
#             self.move(QCursor.pos() - self.click_position)
#             event.accept()

#     def mouseReleaseEvent(self, event):
#         if event.button() == Qt.LeftButton:
#             # Reset the cursor in buttons flag
#             self.cursor_in_buttons = False
#             self.click_position = None
#             event.accept()

# app = QApplication(sys.argv)

# window = MyWindow()
# window.setGeometry(100, 100, 400, 300)
# window.show()

# sys.exit(app.exec())

# =====================================================================================================================================


# import sys
# from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.initUI()

#     def initUI(self):
#         self.setWindowTitle("My Application")

#         # Create the "Load" button and connect it to the openFile function
#         loadButton = QPushButton("Load", self)
#         loadButton.clicked.connect(self.openFile)
#         loadButton.setGeometry(50, 50, 100, 30)

#         self.setGeometry(100, 100, 300, 200)
#         self.show()

#     def openFile(self):
#         options = QFileDialog.Options()
#         fileName, _ = QFileDialog.getOpenFileName(self, "Load File", "", "All Files (*);;Text Files (*.txt)", options=options)
#         if fileName:
#             print("Selected file:", fileName)


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     sys.exit(app.exec_())

# ==================================================================================================================================

# import os
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import letter

# def convert_tab_to_pdf(txt_file, pdf_file):
#     # Read in the text file
#     with open(txt_file, 'r') as f:
#         tab_text = f.read()
    
#     # Create a PDF canvas and set the font
#     pdf_canvas = canvas.Canvas(pdf_file, pagesize=letter)
#     pdf_canvas.setFont("Courier", 10)
    
#     # Split the text into lines and draw them on the PDF canvas
#     lines = tab_text.split('\n')
#     y = 750  # Starting y position for the first line
#     line_index = 0
#     while line_index < len(lines):
#         # Split the line into chunks no wider than 500 pixels
#         chunks = [lines[line_index][i:i+50] for i in range(0, len(lines[line_index]), 50)]
#         if len(chunks) == 1:
#             # If the line has no spaces, write it out in parts every sixth line
#             remaining_chunks = chunks[0]
#             for i in range(line_index, line_index + 6):
#                 if i >= len(lines):
#                     break
#                 if i == line_index:
#                     pdf_canvas.drawString(50, y, remaining_chunks[:50])
#                     remaining_chunks = remaining_chunks[50:]
#                 else:
#                     pdf_canvas.drawString(50, y, remaining_chunks[:50])
#                     remaining_chunks = remaining_chunks[50:]
#                     y -= 12
#         else:
#             # Write out the line normally
#             for chunk in chunks:
#                 pdf_canvas.drawString(50, y, chunk)
#                 y -= 12
#         line_index += 1
    
#     # Save the PDF file
#     pdf_canvas.save()

# # Example usage:
# convert_tab_to_pdf('tab.txt', 'my_tab.pdf')

# ==================================================================================================================================================================================