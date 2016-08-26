import binascii
from bluepy.btle import BTLEException, Peripheral


class Yeelight(object):
    WRITE_CHAR_UUID = "aa7d3f34"  # -2d4f-41e0-807f-52fbf8cf7443"

    COMMAND_STX = "43"
    COMMAND_ETX = "00"

    AUTH_CMD = "67"
    AUTH_ON = "02"

    POWER_CMD = "40"
    POWER_ON = "01"
    POWER_OFF = "02"

    COLOR_CMD = "41"
    RGB_MODE = "65"

    BRIGHT_CMD = "42"

    COLORTEMP_CMD = "43"
    TEMP_MODE = "65"

    COLORFLOW_CMD = "4a"

    SLEEP_CMD = "7f03"

    def __init__(self, address):
        self.__address = address
        self.__connect()


    def __connect(self):
        self.__peripheral = Peripheral(self.__address)
        characteristics = self.__peripheral.getCharacteristics()
        self.__ch = filter(lambda x: binascii.b2a_hex(x.uuid.binVal)
                           .startswith(self.WRITE_CHAR_UUID),
                           characteristics)[0]

        self.__write_cmd(
            self.COMMAND_STX +
            self.AUTH_CMD +
            self.AUTH_ON +
            self.COMMAND_ETX * 15)

    def __write_cmd(self, value):
        for _ in range(3):
            try:
                self.__ch.write(binascii.a2b_hex(value))
            except BTLEException:
                self.__connect()
            else:
                break

    def poweron(self):
        self.__write_cmd(
            self.COMMAND_STX +
            self.POWER_CMD +
            self.POWER_ON +
            self.COMMAND_ETX * 15)

    def poweroff(self):
        self.__write_cmd(
            self.COMMAND_STX +
            self.POWER_CMD +
            self.POWER_OFF +
            self.COMMAND_ETX * 15)

    def setrgb(self, rgb):
        self.__write_cmd(
            self.COMMAND_STX +
            self.COLOR_CMD +
            rgb + '00' +
            self.RGB_MODE +
            self.COMMAND_ETX * 11)

    def setbrightness(self, value):
        self.__write_cmd(
            self.COMMAND_STX +
            self.BRIGHT_CMD +
            ('%02x' % value) +
            self.COMMAND_ETX * 15)

    def setwarm(self, value):
        self.__write_cmd(
            self.COMMAND_STX +
            self.COLORTEMP_CMD +
            ('%04x' % (1700 + value * 4800)) +
            self.TEMP_MODE +
            self.COMMAND_ETX * 13)

    def setsleep(self, minute):
        self.__write_cmd(
            self.COMMAND_STX +
            self.SLEEP_CMD +
            ('%02x' % minute) +
            self.COMMAND_ETX * 14
        )
