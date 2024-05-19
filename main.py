# main.py
import os
import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from Ui_wav_to_c_array import Ui_MainWindow

select_yes_index = 0
select_no_index = 1

save_file_type_txt = '.txt'
save_file_type_c = '.c'


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.pushButton_src_file.clicked.connect(self.select_src_file)
        self.pushButton_src_dir.clicked.connect(self.select_src_dir)
        self.pushButton_dst_dir.clicked.connect(self.select_dst_dir)
        self.pushButton_begin_transfer.clicked.connect(self.begin_transfer)

        self.number_base = 16
        self.max_num_in_line = 16
        self.add_comma = True
        self.transfer_single_file = True
        self.Bytes_in_data = 1
        self.add_wav_header = True
        self.add_c_header = True
        self.save_file_type = save_file_type_c

        self.radioButton_c_file.setChecked(True)
        self.radioButton_c_file.toggled.connect(self.change_save_file_type)
        self.radioButton_src_file.setChecked(True)
        self.radioButton_src_file.toggled.connect(self.change_get_src_method)
        self.change_get_src_method()  # 更新界面显示
        self.radioButton_hex.setChecked(True)
        self.radioButton_hex.toggled.connect(self.change_number_base)
        self.spinBox_byte_number.setValue(self.Bytes_in_data)
        self.spinBox_byte_number.valueChanged.connect(self.change_bytes_in_data)
        self.spinBox_max_num_in_line.setValue(self.max_num_in_line)
        self.spinBox_max_num_in_line.valueChanged.connect(self.change_max_num_in_line)
        self.comboBox_comma_select.setCurrentIndex(0)
        self.comboBox_comma_select.currentIndexChanged.connect(self.change_comma_select)
        self.comboBox_c_name.setCurrentIndex(0)
        self.comboBox_c_name.currentIndexChanged.connect(self.change_c_header_select)
        self.comboBox_wav_header.setCurrentIndex(0)
        self.comboBox_wav_header.currentIndexChanged.connect(self.change_wav_header_select)

        self.lineEdit_src_file.setText('C:/Users/sungu/Desktop/wav/1.wav')
        self.lineEdit_dst_dir.setText('C:/Users/sungu/Desktop/wav')

    def change_get_src_method(self):
        if self.radioButton_src_file.isChecked():
            self.transfer_single_file = True
            self.pushButton_src_file.setEnabled(True)
            self.pushButton_src_dir.setEnabled(False)
        else:
            self.transfer_single_file = False
            self.pushButton_src_dir.setEnabled(True)
            self.pushButton_src_file.setEnabled(False)

    def select_src_file(self):
        if self.lineEdit_src_file.text() == '':
            src_path = os.getcwd()
        else:
            src_path = os.path.dirname(self.lineEdit_src_file.text())

        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', src_path)
        if file_name:
            self.lineEdit_src_file.setText(file_name)

    def select_src_dir(self):
        if self.lineEdit_src_dir.text() == '':
            src_path = os.getcwd()
        else:
            src_path = self.lineEdit_src_dir.text()

        dir_name = QFileDialog.getExistingDirectory(self, 'Select Source Directory', src_path)
        if dir_name:
            self.lineEdit_src_dir.setText(dir_name)

    def select_dst_dir(self):
        if self.lineEdit_dst_dir.text() == '':
            src_path = os.getcwd()
        else:
            src_path = self.lineEdit_dst_dir.text()

        dir_name = QFileDialog.getExistingDirectory(self, "选择保存地址", src_path)
        if dir_name:
            self.lineEdit_dst_dir.setText(dir_name)

    def begin_transfer(self):
        dst_dir = self.lineEdit_dst_dir.text()  # 获取用户选择的目标目录路径

        if not dst_dir:
            QMessageBox.warning(self, "错误", "请先选择目的地址")
            return

        # 如果选择的是源文件
        if self.transfer_single_file:
            src_path = self.lineEdit_src_file.text()  # 获取用户选择的源文件或源文件目录路径
            if not src_path:
                QMessageBox.warning(self, "错误", "请先选择源文件")
                return

            self.convert_wav_to_c_array(src_path, dst_dir)
        # 如果选择的是源目录
        else:
            src_path = self.lineEdit_src_dir.text()  # 获取用户选择的源文件或源文件目录路径
            if not src_path:
                QMessageBox.warning(self, "错误", "请先选择源文件目录")
                return

            for file_name in os.listdir(src_path):
                if file_name.endswith(".wav"):
                    file_path = os.path.join(src_path, file_name)
                    self.convert_wav_to_c_array(file_path, dst_dir)

        QMessageBox.information(self, "完成", "转换完成")

    def change_save_file_type(self):
        if self.radioButton_c_file.isChecked():
            self.save_file_type = save_file_type_c
        else:
            self.save_file_type = save_file_type_txt

    def change_number_base(self):
        if self.radioButton_decimal.isChecked():
            self.number_base = 10
        else:
            self.number_base = 16

    def change_bytes_in_data(self):
        self.Bytes_in_data = self.spinBox_byte_number.value()

    def change_max_num_in_line(self):
        self.max_num_in_line = self.spinBox_max_num_in_line.value()

    def change_wav_header_select(self):
        if self.comboBox_wav_header.currentIndex() == select_yes_index:
            self.add_wav_header = True
        else:
            self.add_wav_header = False

    def change_c_header_select(self):
        if self.comboBox_c_name.currentIndex() == select_yes_index:
            self.add_c_header = True
        else:
            self.add_c_header = False
        print('add_c_header', self.add_c_header)

    def change_comma_select(self):
        if self.comboBox_comma_select.currentIndex() == select_yes_index:
            self.add_comma = True
        else:
            self.add_comma = False

        print('comma_select', self.add_comma)

    def convert_wav_to_c_array(self, wav_file_path, dst_dir):
        import wave
        import numpy as np

        try:
            with wave.open(wav_file_path, 'rb') as wav_file:
                self.textBrowser.append('开始转换：' + wav_file_path)

                n_channels, sampwidth, framerate, n_frames, comptype, compname = wav_file.getparams()

                self.textBrowser.append("n_channels: " + str(n_channels))
                self.textBrowser.append("sampwidth: " + str(sampwidth))
                self.textBrowser.append("framerate: " + str(framerate))
                self.textBrowser.append("n_frames: " + str(n_frames))
                self.textBrowser.append("comptype: " + str(comptype))
                self.textBrowser.append("compname: " + str(compname))

                if sampwidth == 1:
                    dtype = np.uint8
                elif sampwidth == 2:
                    dtype = np.int16
                else:
                    self.textBrowser.append("不支持的样本宽度: {}".format(sampwidth))
                    return

                frames = wav_file.readframes(n_frames * n_channels)

                out_file_name = os.path.join(dst_dir,
                                             os.path.basename(wav_file_path).replace('.wav', self.save_file_type))

                out_file_name = out_file_name.replace('\\', '/')

                if self.save_file_type == save_file_type_txt:
                    audio_data = np.frombuffer(frames, dtype=dtype)
                    try:
                        with open(out_file_name, 'w') as out_file:
                            out_file.write("SAMPLES:" + str(n_frames) + '\n')
                            out_file.write("BITSPERSAMPLE:" + str(sampwidth * 8) + '\n')
                            out_file.write("CHANNELS:" + str(n_channels) + '\n')
                            out_file.write("SAMPLERATE:" + str(framerate) + '\n')
                            out_file.write("NORMALIZED:" + 'FALSE' + '\n')

                            audio_str = [str(value) for value in audio_data.flatten()]

                            for i in range(0, len(audio_str)):
                                out_file.write(audio_str[i] + "\n")

                        self.textBrowser.append("转换完成： " + out_file_name)
                    except Exception as e:
                        self.textBrowser.append("文件写入异常: " + out_file_name + ' ' + str(e))
                else:  # save as c array

                    if self.add_wav_header:
                        with open(wav_file_path, 'rb') as f:
                            frames = f.read()

                    try:
                        with open(out_file_name, 'w') as out_file:
                            if sampwidth == 1 or self.Bytes_in_data == 1:
                                audio_data = np.frombuffer(frames, dtype=np.uint8)
                            else:
                                if self.number_base == 16:
                                    audio_data = np.frombuffer(frames, dtype=np.uint16)
                                else:
                                    audio_data = np.frombuffer(frames, dtype=np.int16)

                            if self.add_c_header:
                                if self.Bytes_in_data == 1:
                                    if self.number_base == 16:
                                        out_file.write("const uint8_t audio_data[] = {\n")
                                    else:
                                        out_file.write("const int8_t audio_data[] = {\n")
                                else:
                                    if self.number_base == 16:
                                        out_file.write("const uint16_t audio_data[] = {\n")
                                    else:
                                        out_file.write("const int16_t audio_data[] = {\n")

                            if self.number_base == 16:
                                # 将数据转换为16进制字符串并每16个数字后加换行符
                                audio_str = [f"0x{value:02X}" if self.Bytes_in_data == 1 else f"0x{value:04X}" for value in audio_data.flatten()]
                            else:
                                audio_str = [f"{value:2d}" if self.Bytes_in_data == 1 else f"{value:4d}" for value in audio_data.flatten()]

                            for i in range(0, len(audio_str), self.max_num_in_line):
                                if self.add_comma:
                                    out_file.write(", ".join(audio_str[i:i + self.max_num_in_line]) + ",\n")
                                else:
                                    out_file.write(" ".join(audio_str[i:i + self.max_num_in_line]) + "\n")

                            if self.add_c_header:
                                out_file.write("};")
                        self.textBrowser.append("转换完成： " + out_file_name)
                    except Exception as e:
                        self.textBrowser.append("文件写入异常: " + out_file_name + ' ' + str(e))

        except wave.Error as e:
            self.textBrowser.append("WAV 文件处理异常: " + str(e))
        except Exception as e:
            self.textBrowser.append("文件处理异常: " + str(e))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
