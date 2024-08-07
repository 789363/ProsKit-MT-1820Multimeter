import serial
import time

class MT1820:
    UNIT_MAP = {
        0x0020: {'unit': 'resistance', 'symbol': 'Ohm', 'factor': 1E-1},
        0x2020: {'unit': 'resistance', 'symbol': 'kOhm', 'factor': 1E-2},
        0x1020: {'unit': 'resistance', 'symbol': 'MOhm', 'factor': 1E-3},
        0x0002: {'unit': 'temperature', 'symbol': '˚C', 'factor': 1E-1},
        0x0001: {'unit': 'temperature', 'symbol': '˚F', 'factor': 1},
        0x4080: {'unit': 'voltage', 'symbol': 'mV', 'factor': 1E-1},
        0x0080: {'unit': 'voltage', 'symbol': 'V', 'factor': 1},
        0x8040: {'unit': 'current', 'symbol': 'μA', 'factor': 1E-6},
        0x4040: {'unit': 'current', 'symbol': 'mA', 'factor': 1E-3},
        0x0040: {'unit': 'current', 'symbol': 'A', 'factor': 1},
        0x0480: {'unit': 'diode-test', 'symbol': 'V', 'factor': 1},
        0x0004: {'unit': 'capacitance', 'symbol': 'nF', 'factor': 1E-2},
        0x8004: {'unit': 'capacitance', 'symbol': 'μF', 'factor': 1E-6},
        0x0010: {'unit': 'transistor-test', 'symbol': 'hFE', 'factor': 1},
        0x0008: {'unit': 'frequency', 'symbol': 'Hz', 'factor': 1E-2},
        0x2008: {'unit': 'frequency', 'symbol': 'kHz', 'factor': 1E3},
        0x1008: {'unit': 'frequency', 'symbol': 'MHz', 'factor': 1E6},
        0x0820: {'unit': 'continuity-test', 'symbol': 'Ohm', 'factor': 1},
    }
    
    FLAGS_MAP = {
        0x2900: {'desc': 'AC'},  # 交流
        0x3100: {'desc': 'DC'},  # 直流
    }
    
    def __init__(self, port='COM3', baudrate=2400):
        self.port = serial.Serial(port, baudrate=baudrate, timeout=1)
    
    def parse_data(self, data):
        if not data:
            return 'Error'  # 如果没有读到数据，返回Error
        
        if data.startswith(b'+?'):
            return 'Error'  # 如果数据不合法，返回Error

        try:
            string_value = data[:5].decode('iso-8859-1').strip().replace('\r', '').replace('\n', '')
            if string_value == "":
                return 'Error'  # 如果数据解析后为空，返回Error

            # 尝试解析数值
            decimal_point = int(data[6])
            try:
                value = float(string_value[:decimal_point] + '.' + string_value[decimal_point:])
                if value != 0:
                    return 'Fail'  # 数值不等于0，返回Fail
                else:
                    return 'Pass'  # 数值等于0，返回Pass
            except ValueError:
                return 'Error'  # 数值转换失败，返回Error
        except Exception as e:
            return 'Error'  # 处理数据时出现任何异常，返回Error
    
    def read_data(self):
        try:
            while True:
                data = self.port.read(32)  # 读取32字节
                result = self.parse_data(data)
                print(result)  # 打印结果
        except serial.SerialException:
            print('Error')  # 串口读取失败

if __name__ == "__main__":
    multimeter = MT1820('COM3', 2400)
    multimeter.read_data()
