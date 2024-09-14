import sys

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (QApplication, QLabel, QPushButton, QVBoxLayout,
                             QWidget)
from streaming import start_streaming, stop_streaming


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Crown Recorder'
        self.left = 100
        self.top = 100
        self.width = 300
        self.height = 200
        self.streaming_process = False
        self.time_elapsed = 0
        self.timer_visible = False
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        layout = QVBoxLayout()

        self.state_label = QLabel('<html>State:<br><b><font color="green">READY</font></b></html>', self)
        self.state_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.state_label)

        self.timer_label = QLabel('Recording time:\n00:00:00', self)
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.hide()  # Initially hide the timer label
        layout.addWidget(self.timer_label)

        self.button = QPushButton('Start recording', self)
        self.button.clicked.connect(self.toggle_server)
        layout.addWidget(self.button)

        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        self.show()

    def format_timer(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def update_timer(self):
        self.time_elapsed += 1
        formatted_timer = self.format_timer(self.time_elapsed)
        self.timer_label.setText(f'Recording time:\n{formatted_timer}')

    def toggle_server(self):
        if not self.streaming_process:
            self.start_streaming()
        else:
            self.stop_streaming()

    def start_streaming(self):
        print("Start streaming...")
        start_streaming()
        self.streaming_process = True
        self.state_label.setText('<html>State:<br><b><font color="red">RECORDING...</font></b></html>')
        self.button.setText('Stop recording')
        if not self.timer_visible:
            self.timer_label.show()
            self.timer_visible = True
        self.timer.start(1000)  # Update every second

    def stop_streaming(self):
        print("Stop streaming...")
        stop_streaming()
        self.streaming_process = False
        self.state_label.setText('<html>State:<br><b><font color="green">READY</font></b></html>')
        self.button.setText('Start recording')
        self.timer.stop()
        self.time_elapsed = 0
        self.timer_label.setText('Recording time:\n00:00:00')
        # We don't hide the timer label once it's been shown

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())