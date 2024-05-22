import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
from psutil import disk_partitions
from PyQt5.QtGui import QTextCursor

try:
    from usb_trace_tool.Ui_usb_trace_tool import Ui_MainWindow
    from usb_trace_tool.u_disk import UsbPortThread, open_usb_port, check_usb_vendor_info
except:
    from Ui_usb_trace_tool import Ui_MainWindow
    from u_disk import UsbPortThread, open_usb_port, check_usb_vendor_info


class UsbTraceWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.start_usb_thread = None
        self.start_usb_identifier = None
        self.usb_ports = []

        self.pushButton_clear.clicked.connect(self.clear_log_win)
        self.pushButton_start.clicked.connect(self.start_usb_trace)
        self.pushButton_stop.clicked.connect(self.stop_usb_trace)

        self.check_usb_ports()
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.check_ports_change)
        self.refresh_timer.start(1000)

    def clear_log_win(self):
        self.plainTextEdit.clear()

    def update_receive_data(self, time, receive_data):
        cursor = self.plainTextEdit.textCursor()
        cursor.movePosition(QTextCursor.End)  # 移动光标到文本末尾

        if self.checkBox_showtime.isChecked():
            cursor.insertText(time + ': '+ receive_data)
        else:
            cursor.insertText(receive_data)

        # 设置滚动条位置到最底部
        self.plainTextEdit.verticalScrollBar().setValue(
            self.plainTextEdit.verticalScrollBar().maximum()
        )

    def start_usb_trace(self):
        port_identifier = self.comboBox.currentText()
        if port_identifier in self.usb_ports and self.start_usb_identifier is None:
            thread = UsbPortThread(port_identifier)
            thread.receive_signal.connect(self.update_receive_data)
            thread.start()
            self.start_usb_thread = thread
            self.start_usb_identifier = port_identifier

    def stop_usb_trace(self):
        if self.start_usb_thread:
            self.start_usb_thread.stop()
            self.start_usb_thread.wait()
            self.start_usb_thread = None
            self.start_usb_identifier = None

    def check_ports_change(self):
        self.check_usb_ports()

    def check_usb_ports(self):
        # 获取当前系统的磁盘分区列表
        partitions = disk_partitions(all=False)
        # 创建一个集合来存储满足条件的磁盘设备名称
        current_ports = set()
        # 遍历所有磁盘分区
        for partition in partitions:
            # 假设分区有一个属性 'opts' 可以检查
            # 检查分区是否是可移动设备
            if 'removable' in partition.opts:
                # 如果分区满足条件，将其设备名称添加到集合中
                current_ports.add(partition.device)

        existing_ports = set(port for port in self.usb_ports)

        # 获取新添加的串口
        new_ports = set(current_ports) - existing_ports
        for port_name in new_ports:
            if check_usb_vendor_info(port_name):
                self.comboBox.addItem(port_name)
                self.usb_ports.append(port_name)

        # 获取已移除的串口
        removed_ports = existing_ports - set(current_ports)
        for port_name in removed_ports:
            if port_name in self.usb_ports:
                if port_name == self.start_usb_identifier:
                    self.stop_usb_trace()

                self.usb_ports.remove(port_name)
                index = self.comboBox.findText(port_name)  # 查找串口名称在 ComboBox 中的索引
                if index != -1:  # 如果找到了对应的索引
                    self.comboBox.removeItem(index)  # 使用索引移除项


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = UsbTraceWindow()
    mainWindow.show()
    sys.exit(app.exec_())
