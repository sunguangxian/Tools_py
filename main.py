import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt

from Ui_main import Ui_Form
from wav_to_array import WavToArrayWindow

       

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.pushButton_wav_to_array.clicked.connect(self.wav_to_array_click)
        self.is_window_open = False

    def wav_to_array_click(self):
        if not self.is_window_open:
            self.wav_to_array_window = WavToArrayWindow()
            self.wav_to_array_window.show()
            self.is_window_open = True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())