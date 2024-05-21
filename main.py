import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from Ui_main import Ui_Form
from sine_wave_generate import SineWaveGenerateWindow
from usb_trace_tool.usb_trace_tool import UsbTraceWindow
from wav_to_array import WavToArrayWindow


class MainWindow(QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.sine_wave_generate_window = None
        self.wav_to_array_window = None
        self.usb_trace_window = None

        self.pushButton_wav_to_array.clicked.connect(self.open_window)
        self.pushButton_sine_wave_generate.clicked.connect(self.open_window)
        self.pushButton_usb_trace.clicked.connect(self.open_window)

    def open_window(self):
        sender = self.sender()
        if sender == self.pushButton_wav_to_array:
            if not self.wav_to_array_window:
                self.wav_to_array_window = WavToArrayWindow()
            self.wav_to_array_window.show()
        elif sender == self.pushButton_sine_wave_generate:
            if not self.sine_wave_generate_window:
                self.sine_wave_generate_window = SineWaveGenerateWindow()
            self.sine_wave_generate_window.show()
        elif sender == self.pushButton_usb_trace:
            if not self.usb_trace_window:
                self.usb_trace_window = UsbTraceWindow()
            self.usb_trace_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
