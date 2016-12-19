import binascii
import struct

from bluepy.btle import BTLEException, DefaultDelegate, Peripheral
class Yeelight(DefaultDelegate):
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

    STATUS_CMD = "44"

    COLORFLOW_CMD = "4a"

    SLEEP_CMD = "7f03"

    def __init__(self, address):
        DefaultDelegate.__init__(self)
        self.__address = address
        self.__connect()

    # Override
    def handleNotification(self, handle, data):
        if handle == 21:
            val = binascii.b2a_hex(data)
            format = (
                '!xx' # 4345 header
                'B' # switch: 01=on 02=off
                'B' # mode: 01=rgb 02=warm
                'BBBx' # RGB
                'B' # Brightness
                'H' # temp 2byte 1700 ~ 6500
                'xxxxxxx'
            )
            (switch, mode, r, g, b,
             brightness, temp) = struct.unpack(format, data)
            if switch != 4:
                self._switch = switch
                self._mode = mode
                self._rgb = '{:02x}{:02x}{:02x}'.format(r, g, b)
                self._temp = temp
                self._brightness = brightness

    def __connect(self):
        self.__peripheral = Peripheral(self.__address)
        self.__peripheral.setDelegate(self)
        characteristics = self.__peripheral.getCharacteristics()
        self.__ch = filter(lambda x: binascii.b2a_hex(x.uuid.binVal)
                           .startswith(self.WRITE_CHAR_UUID),
                           characteristics)[0]

        # Register notification
        self.__peripheral.writeCharacteristic(
            0x16,
            binascii.a2b_hex('0100'))

        # Auth
        self.__write_cmd(
            self.COMMAND_STX +
            self.AUTH_CMD +
            self.AUTH_ON +
            self.COMMAND_ETX * 15)

        # Get status
        self.__write_cmd(
            self.COMMAND_STX +
            self.STATUS_CMD +
            self.COMMAND_ETX * 16
        )

    def __write_cmd(self, value):
        for _ in range(3):
            try:
                self.__ch.write(binascii.a2b_hex(value))
                self.__peripheral.waitForNotifications(1.0)
            except BTLEException:
                self.__connect()
            else:
                break

    @property
    def switch(self):
        self.update_status()
        return self._switch

    @property
    def brightness(self):
        self.update_status()
        return self._brightness

    @property
    def temp(self):
        self.update_status()
        return self._temp

    @property
    def rgb(self):
        self.update_status()
        return self._rgb

    @property
    def mode(self):
        self.update_status()
        return self._mode

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

    def set_rgb(self, rgb):
        self.__write_cmd(
            self.COMMAND_STX +
            self.COLOR_CMD +
            rgb + '00' +
            self.RGB_MODE +
            self.COMMAND_ETX * 11)

    def set_brightness(self, value):
        self.__write_cmd(
            self.COMMAND_STX +
            self.BRIGHT_CMD +
            ('%02x' % value) +
            self.COMMAND_ETX * 15)

    def set_temp(self, value):
        if not 1700 <= value <= 6500 and 0.0 <= value <= 1.0:
            value = 1700 + value * 4800

        self.__write_cmd(
            self.COMMAND_STX +
            self.COLORTEMP_CMD +
            ('%04x' % value) +
            self.TEMP_MODE +
            self.COMMAND_ETX * 13)

    def set_sleep(self, minute):
        self.__write_cmd(
            self.COMMAND_STX +
            self.SLEEP_CMD +
            ('%02x' % minute) +
            self.COMMAND_ETX * 14
        )

    def update_status(self):
        self.__peripheral.waitForNotifications(0.01)
