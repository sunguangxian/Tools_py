import sys
import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIntValidator, QValidator
from PyQt5.QtWidgets import QApplication
from matplotlib import pyplot as plt
from Ui_sine_wave_generate import Ui_MainWindow  # 假设您的 UI 文件是这样命名的

class SineWaveGenerateWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.sin_wave_int = None
        self.setupUi(self)


        self.pushButton_show.setDisabled(True)
        self.pushButton_generate.clicked.connect(self.generate_sine_wave)
        self.pushButton_show.clicked.connect(self.show_plot)

    def generate_sine_wave(self):
        self.textBrowser.clear()

        sample_rate = self.spinBox_samplerate.value()
        amplitude = self.spinBox_amplitude.value()
        # 生成0到sample_rate-1的数组
        x = np.arange(sample_rate * self.spinBox_cycle.value())

        # 计算正弦波数据，并映射到DAC的范围
        sin_wave = np.sin(2 * np.pi * x / sample_rate) * amplitude

        # 将数据转换为整数类型
        self.sin_wave_int = sin_wave.astype(np.int16)

        # 生成 C 语言数组格式的字符串
        sin_wave_str = 'const int16_t ' + 'sin_wave_' + str(sample_rate) + 'K' + '[] = {\n'
        sin_wave_str += ', '.join(map(str, self.sin_wave_int))
        sin_wave_str += '\n};'

        self.textBrowser.insertPlainText(sin_wave_str)

        self.pushButton_show.setEnabled(True)

    def show_plot(self):
        # 绘制波形图
        plt.plot(self.sin_wave_int, linewidth=2, color='b', linestyle='-', marker='o', markersize=5, label='Sine Wave')
        plt.title('Sine Wave Data')
        plt.xlabel('Sample Number')
        plt.ylabel('DAC Value')
        plt.legend()
        plt.grid(True)
        # for i, value in enumerate(self.sin_wave_int):
        #    plt.annotate(str(value), (i, value), xytext=(i, value + 100), 
        #                ha='center', fontsize=8, rotation=45)  # 旋转文本

        plt.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SineWaveGenerateWindow()
    window.show()
    sys.exit(app.exec_())
