import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication

try:
    from string_transfer.Ui_string_transfer import Ui_MainWindow
except ImportError:
    from Ui_string_transfer import Ui_MainWindow


class strtransferwindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton_hex_to_string.clicked.connect(self.hex_to_str)
        self.pushButton_clear_src.clicked.connect(self.clear_text)
        self.pushButton_copy_dst.clicked.connect(self.copy_dst_text)

    def clear_text(self):
        self.textBrowser_src.clear()
        self.textBrowser_dst.clear()

    def copy_dst_text(self):
        self.textBrowser_dst.copy()

    def reformat_text(self, char_list, line_length=16):
        # 将列表中的字符用空格连接起来
        # joined_chars = ' '.join(char_list)
        # print(f'joined_chars: {joined_chars}')

        # 每16个字符插入一个换行符
        # 首先按空格分割字符，以便重组为需要的格式
        # split_chars = joined_chars.split(' ')
        # print(split_chars)
        formatted_str = ''
        for i in range(0, len(char_list), 16):
            formatted_str += ' '.join(char_list[i:i + 16]) + '\n'



        return formatted_str

    def hex_to_str(self):

        hex_str = self.textBrowser_src.toPlainText().strip()
        hex_str = hex_str.split(' ')

        self.textBrowser_src.clear()
        self.textBrowser_dst.clear()

        padded_hex_str = [x.zfill(2) for x in hex_str]

        formatted_str = ''
        for i in range(0, len(padded_hex_str), 16):
            formatted_str += ' '.join(padded_hex_str[i:i + 16]) + '\n'
        self.textBrowser_src.insertPlainText(formatted_str)

        formatted_str = ''
        for i in range(0, len(padded_hex_str), 16):
            chr_str = []
            for j in range(0, 16):
                # 检查索引是否超出范围
                if i + j < len(padded_hex_str):
                    chr_str.append(chr(int(padded_hex_str[i + j], 16)))

            formatted_str += ' '.join(chr_str[0: 16]) + '\n'

        self.textBrowser_dst.insertPlainText(formatted_str)







if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = strtransferwindow()
    window.show()
    sys.exit(app.exec_())
