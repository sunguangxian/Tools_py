import ctypes
import datetime
# 引入 ctypes 中的结构体类型和基本数据类型
from ctypes import Structure, c_ubyte, c_ulong, c_void_p, wintypes, c_ushort
import time

from PyQt5.QtCore import QThread, pyqtSignal

# 导入必要的 Windows API 函数和常量
kernel32 = ctypes.WinDLL('kernel32')
DeviceIoControl = kernel32.DeviceIoControl
CreateFile = kernel32.CreateFileW

# 定义常量
# 设备访问模式
GENERIC_READ = 0x80000000
GENERIC_WRITE = 0x40000000
# 共享模式
FILE_SHARE_READ = 0x00000001
FILE_SHARE_WRITE = 0x00000002
# 打开选项
OPEN_EXISTING = 3

INVALID_HANDLE_VALUE = -1

FILE_DEVICE_MASS_STORAGE = 0x0000002d
IOCTL_STORAGE_BASE = FILE_DEVICE_MASS_STORAGE

IOCTL_SCSI_BASE = 0x0004  # SCSI设备

METHOD_BUFFERED = 0x00  # 使用缓冲传输
METHOD_IN_DIRECT = 0x01  # 直接输入方法
METHOD_OUT_DIRECT = 0x02  # 直接输出方法
METHOD_NEITHER = 0x03  # 无缓冲直接传输

FILE_ANY_ACCESS = 0  # 表示任何访问权限。这个常量的值为 0，通常用于指定无需特殊访问权限的操作。
FILE_SPECIAL_ACCESS = FILE_ANY_ACCESS  # 表示特殊访问权限。这个常量是 FILE_ANY_ACCESS 的别名，因此其值也是 0。
FILE_READ_ACCESS = 0x0001  # 表示读取权限。这个常量的值为 0x0001，用于指定操作需要读取数据的权限。
FILE_WRITE_ACCESS = 0x0002  # 表示写入权限。这个常量的值为 0x0002，用于指定操作需要写入数据的权限。

SCSI_PASS_THROUGH_CODE = 0x0405
STORAGE_QUERY_PROPERTY = 0x0500

SCSI_IOCTL_DATA_OUT = 0
SCSI_IOCTL_DATA_IN = 1
SCSI_IOCTL_DATA_UNSPECIFIED = 2


def CTL_CODE(device_type, function, method, access):
    # 计算控制码
    control_code = ((device_type << 16) | (access << 14) | (function << 2) | method)
    return control_code


IOCTL_SCSI_PASS_THROUGH_DIRECT = CTL_CODE(IOCTL_SCSI_BASE, SCSI_PASS_THROUGH_CODE, METHOD_BUFFERED,
                                          FILE_READ_ACCESS | FILE_WRITE_ACCESS)

IOCTL_STORAGE_QUERY_PROPERTY = CTL_CODE(IOCTL_STORAGE_BASE, STORAGE_QUERY_PROPERTY, METHOD_BUFFERED,
                                        FILE_ANY_ACCESS)


# 定义 SCSI_PASS_THROUGH_DIRECT 结构体
class SCSI_PASS_THROUGH_DIRECT(Structure):
    _fields_ = [
        ("Length", c_ushort),
        ("ScsiStatus", c_ubyte),
        ("PathId", c_ubyte),
        ("TargetId", c_ubyte),
        ("Lun", c_ubyte),
        ("CdbLength", c_ubyte),
        ("SenseInfoLength", c_ubyte),
        ("DataIn", c_ubyte),
        ("DataTransferLength", c_ulong),
        ("TimeOutValue", c_ulong),
        ("DataBuffer", c_void_p),
        ("SenseInfoOffset", c_ulong),
        ("Cdb", c_ubyte * 16)
    ]


# 定义 SCSI_PASS_THROUGH_DIRECT_WITH_BUFFER 结构体
class SCSI_PASS_THROUGH_DIRECT_WITH_BUFFER(Structure):
    _fields_ = [
        ("sptd", SCSI_PASS_THROUGH_DIRECT),
        ("ucSenseBuf", c_ubyte * 24),
        ("ucDataBuf", c_ubyte * (64 * 1024))
    ]


# Define structures
class STORAGE_PROPERTY_QUERY(ctypes.Structure):
    _fields_ = [
        ('PropertyId', wintypes.DWORD),
        ('QueryType', wintypes.DWORD),
        ('AdditionalParameters', wintypes.BYTE * 1),
    ]


class STORAGE_DEVICE_DESCRIPTOR(ctypes.Structure):
    _fields_ = [
        ('Version', wintypes.DWORD),  # DWORD 类型，用 ctypes.c_ulong 或 wintypes.DWORD 表示
        ('Size', wintypes.DWORD),  # DWORD 类型，用 ctypes.c_ulong 或 wintypes.DWORD 表示
        ('DeviceType', wintypes.BYTE),  # BYTE 类型，用 ctypes.c_ubyte 或 wintypes.BYTE 表示
        ('DeviceTypeModifier', wintypes.BYTE),  # BYTE 类型，用 ctypes.c_ubyte 或 wintypes.BYTE 表示
        ('RemovableMedia', wintypes.BOOLEAN),  # BOOLEAN 类型，用 ctypes.c_bool 或 wintypes.BOOL 表示
        ('CommandQueueing', wintypes.BOOLEAN),  # BOOLEAN 类型，用 ctypes.c_bool 或 wintypes.BOOL 表示
        ('VendorIdOffset', wintypes.DWORD),  # DWORD 类型，用 ctypes.c_ulong 或 wintypes.DWORD 表示
        ('ProductIdOffset', wintypes.DWORD),  # DWORD 类型，用 ctypes.c_ulong 或 wintypes.DWORD 表示
        ('ProductRevisionOffset', wintypes.DWORD),  # DWORD 类型，用 ctypes.c_ulong 或 wintypes.DWORD 表示
        ('SerialNumberOffset', wintypes.DWORD),  # DWORD 类型，用 ctypes.c_ulong 或 wintypes.DWORD 表示
        ('BusType', wintypes.BYTE),  # STORAGE_BUS_TYPE 类型，用 ctypes.c_int 或 wintypes.DWORD 表示
        ('RawPropertiesLength', wintypes.DWORD),  # DWORD 类型，用 ctypes.c_ulong 或 wintypes.DWORD 表示
        ('RawDeviceProperties', wintypes.BYTE * 1),  # BYTE 类型数组，用 ctypes.c_ubyte 或 wintypes.BYTE 表示
    ]


def open_usb_port(port_identifier):
    # 获取所有逻辑驱动器的位掩码
    logical_drives_mask = kernel32.GetLogicalDrives()

    # 遍历所有逻辑驱动器
    for drive_number in range(26):  # 0 到 25 对应 A 到 Z 盘符
        if logical_drives_mask & (1 << drive_number):
            # 将驱动器编号转换为盘符（例如，0 -> 'A:', 1 -> 'B:', 等）
            drive_letter = chr(ord('A') + drive_number)
            if drive_letter in port_identifier:
                device_path = f"\\\\.\\{drive_letter}:"
                # 调用 CreateFile 函数获取指定盘符的设备句柄
                device_handle = CreateFile(
                    device_path,
                    GENERIC_READ | GENERIC_WRITE,
                    FILE_SHARE_READ | FILE_SHARE_WRITE,
                    None,
                    OPEN_EXISTING,
                    0,
                    None
                )

                return device_handle

    return INVALID_HANDLE_VALUE

def check_usb_vendor_info(port_identifier):
    device_handle = open_usb_port(port_identifier)
    if device_handle == INVALID_HANDLE_VALUE:
        return False

    query = STORAGE_PROPERTY_QUERY()
    query.PropertyId = 0  # STORAGE_DEVICE_PROPERTY
    query.QueryType = 0  # PropertyStandardQuery

    # Create storage device descriptor
    device_descriptor = STORAGE_DEVICE_DESCRIPTOR()
    device_descriptor.Size = ctypes.sizeof(STORAGE_DEVICE_DESCRIPTOR)

    buffer = ctypes.create_string_buffer(512)

    # Call DeviceIoControl
    bytes_returned = wintypes.DWORD()
    success = DeviceIoControl(
        device_handle,
        IOCTL_STORAGE_QUERY_PROPERTY,
        ctypes.byref(query),
        ctypes.sizeof(query),
        buffer,
        len(buffer),
        ctypes.byref(bytes_returned),
        None
    )

    if success:
        device_descriptor = ctypes.cast(buffer, ctypes.POINTER(STORAGE_DEVICE_DESCRIPTOR)).contents

        # Extract the vendor information using the VendorIdOffset
        vendor_offset = device_descriptor.VendorIdOffset
        if vendor_offset > 0:
            # 获取 device_descriptor 指针的地址
            base_address = ctypes.addressof(device_descriptor)

            # 计算供应商信息在缓冲区中的地址
            vendor_info_address = base_address + vendor_offset

            # 将地址转换为 ctypes.c_char_p 类型的指针
            vendor_info_ptr = ctypes.cast(vendor_info_address, ctypes.c_char_p)

            # 解码供应商信息为 ASCII 字符串，并去除两端空格
            vendor_info = vendor_info_ptr.value.decode('ascii').strip()

            # if 'KIRISUNC' in vendor_info:
            return True

    return False


class UsbPortThread(QThread):
    receive_signal = pyqtSignal(str, str)  # 信号，用于发送接收到的数据和串口标识符
    def __init__(self, port_identifier):
        super().__init__()
        self.port_instance = INVALID_HANDLE_VALUE
        self.port_identifier = port_identifier

    def run(self):
        self.port_instance = open_usb_port(self.port_identifier)
        self.receive_data()

    def stop(self):
        if self.port_instance is not INVALID_HANDLE_VALUE:
            # 关闭设备句柄
            kernel32.CloseHandle(self.port_instance)
            self.port_instance = INVALID_HANDLE_VALUE
        self.quit()

    def receive_data(self):
        while self.port_instance is not INVALID_HANDLE_VALUE:
            try:
                time.sleep(0.5)  # 0.5s

                receive_len = 128

                data = self.usb_receive_message(receive_len)

                # 获取当前时间，精确到毫秒
                current_time = datetime.datetime.now()
                # 格式化时间字符串，显示到毫秒级别
                formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

                self.receive_signal.emit(formatted_time, data)

            except Exception as e:
                print(f"读取数据时发生异常: {e}")
                break

    def usb_receive_message(self, receive_len):
        # 准备 SCSI_PASS_THROUGH 结构
        spt = SCSI_PASS_THROUGH_DIRECT_WITH_BUFFER()
        spt.sptd.Length = ctypes.sizeof(SCSI_PASS_THROUGH_DIRECT)
        spt.sptd.PathId = 0
        spt.sptd.TargetId = 1
        spt.sptd.Lun = 0
        spt.sptd.CdbLength = 10  # CDB 长度，根据您的 SCSI 命令设置
        spt.sptd.DataIn = SCSI_IOCTL_DATA_IN  # 设置为 1 表示数据传输方向为读取
        spt.sptd.SenseInfoLength = 24
        spt.sptd.DataTransferLength = receive_len  # 设置数据传输长度，根据需要调整
        spt.sptd.TimeOutValue = 2  # 设置超时时间为 2 秒

        # 定义长度为 64 * 1024 + 10 的 BYTE 数组
        data_buff = (ctypes.c_ubyte * receive_len)()
        # 使用 ctypes.cast 将数组的指针转换为 c_void_p 类型
        data_buff_ptr = ctypes.cast(data_buff, ctypes.c_void_p)

        spt.sptd.DataBuffer = data_buff_ptr

        # 使用 ctypes.addressof 获取结构体实例和成员变量的地址
        struct_start_address = ctypes.addressof(spt)
        ucSenseBuf_address = ctypes.addressof(spt.ucSenseBuf)
        # 计算 ucSenseBuf 在结构体中的偏移量
        ucSenseBuf_offset = ucSenseBuf_address - struct_start_address
        # 设置 sptdwb.sptd.SenseInfoOffset 字段
        spt.sptd.SenseInfoOffset = ucSenseBuf_offset

        # 设置 SCSI 命令（例如，SCSI 读取命令）
        spt.sptd.Cdb = (0x98, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

        length = ctypes.sizeof(SCSI_PASS_THROUGH_DIRECT_WITH_BUFFER)

        # 调用 DeviceIoControl 发送 SCSI 命令
        bytes_returned = wintypes.DWORD()
        try:
            success = DeviceIoControl(
                self.port_instance,
                IOCTL_SCSI_PASS_THROUGH_DIRECT,
                ctypes.byref(spt),
                length,
                ctypes.byref(spt),
                length,
                ctypes.byref(bytes_returned),
                None
            )
        except Exception as e:
            print(f"读取数据时发生异常: {e}")

        if success:
            # 打印接收到的数据
            '''
            print("接收到的数据:")
            for index, byte in enumerate(data_buff):
                # 使用 %02X 格式化字节数据为十六进制形式
                print(f"{byte:02X} ", end="")

                # 每16个字节换行
                if (index + 1) % 16 == 0:
                    print()
            '''
            return data_buff

        else:
            error = kernel32.GetLastError()
            print(f"SCSI 命令发送失败: {error}")
            return None

    def usb_send_message(self, data):
        # 准备 SCSI_PASS_THROUGH 结构
        spt = SCSI_PASS_THROUGH_DIRECT_WITH_BUFFER()
        spt.sptd.Length = ctypes.sizeof(SCSI_PASS_THROUGH_DIRECT)
        spt.sptd.PathId = 0
        spt.sptd.TargetId = 1
        spt.sptd.Lun = 0
        spt.sptd.CdbLength = 10  # CDB 长度，根据您的 SCSI 命令设置
        spt.sptd.DataIn = SCSI_IOCTL_DATA_OUT  # 设置为 1 表示数据传输方向为读取
        spt.sptd.SenseInfoLength = 24
        spt.sptd.DataTransferLength = len(data)  # 设置数据传输长度，根据需要调整
        spt.sptd.TimeOutValue = 2  # 设置超时时间为 2 秒

        # 定义长度为 64 * 1024 + 10 的 BYTE 数组
        msg = (ctypes.c_ubyte * len(data))(*data)
        # 使用 ctypes.cast 将数组的指针转换为 c_void_p 类型
        data_buff_ptr = ctypes.cast(msg, ctypes.c_void_p)

        spt.sptd.DataBuffer = data_buff_ptr

        # 使用 ctypes.addressof 获取结构体实例和成员变量的地址
        struct_start_address = ctypes.addressof(spt)
        ucSenseBuf_address = ctypes.addressof(spt.ucSenseBuf)
        # 计算 ucSenseBuf 在结构体中的偏移量
        ucSenseBuf_offset = ucSenseBuf_address - struct_start_address
        # 设置 sptdwb.sptd.SenseInfoOffset 字段
        spt.sptd.SenseInfoOffset = ucSenseBuf_offset

        # 设置 SCSI 命令（例如，SCSI 读取命令）
        spt.sptd.Cdb = (0x9A, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

        length = ctypes.sizeof(SCSI_PASS_THROUGH_DIRECT_WITH_BUFFER)

        # 调用 DeviceIoControl 发送 SCSI 命令
        bytes_returned = wintypes.DWORD()

        success = DeviceIoControl(
            self.port_instance,
            IOCTL_SCSI_PASS_THROUGH_DIRECT,
            ctypes.byref(spt),
            length,
            ctypes.byref(spt),
            length,
            ctypes.byref(bytes_returned),
            None
        )

        if success:
            return
            #print(f"SCSI 命令发送成功")
            # 处理返回数据
            # 您可以在 data_buffer 中查看返回数据
        else:
            error = kernel32.GetLastError()
            print(f"SCSI 命令发送失败: {error}")
