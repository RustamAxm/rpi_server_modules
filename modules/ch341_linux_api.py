from smbus2 import SMBus, i2c_msg


class ONET8501:
    def __init__(self, bus_=17, address=0x44):
        self.bus = SMBus(bus_)
        self.i2c_addr = address

    def readReg(self, register):
        return self.bus.read_byte_data(self.i2c_addr, register)

    def writeReg(self, register, value):
        self.bus.write_byte_data(self.i2c_addr, register, value)

    def set_control_settings(self, data):
        self.write(0x00, 0)

    def get_control_settings(self):
        pass

    def read(self, register):
        return self.bus.read_byte_data(self.i2c_addr, register)

    def write(self, register, value):
        return self.bus.write_byte_data(self.i2c_addr, register, value)


if __name__ == '__main__':
    mon1 = ONET8501(bus_=17, address=0x44)
    mon2 = ONET8501(bus_=18, address=0x44)
    for i in range(16):
        print(mon1.read(i))

    for i in range(16):
        print(mon2.read(i))