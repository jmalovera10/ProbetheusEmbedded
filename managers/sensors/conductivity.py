import serial
from serial import SerialException


class ConductivityManager:

    def __init__(self):
        try:
            self.serial = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1)
            self.wakeup_device()
        except SerialException as e:
            print("Error, ", e)

    def begin_continuous_readings(self):
        try:
            self.send_command('C,1')
            self.serial.flush()
            return True
        except SerialException as e:
            print("Error, ", e)
            return None

    def stop_continuous_readings(self):
        try:
            self.send_command('C,0')
            self.serial.flush()
            return True
        except SerialException as e:
            print ("Error, ", e)
            return None

    def make_reading(self):
        try:
            self.send_command('R')
            lines = self.read_lines()
            return lines
        except SerialException as e:
            print("Error, ", e)
            return None

    def sleep_device(self):
        try:
            self.send_command('Sleep')
            response = self.read_lines()
            print('SLEEP: ', response)
            return True
        except SerialException as e:
            print("Error, ", e)
            return None

    def wakeup_device(self):
        try:
            self.send_command('i')
            response = self.read_lines()
            print('WAKEUP: ', response)
        except SerialException as e:
            print("Error, ", e)
            return None

    def send_command(self, command):
        buf = command + '\r'
        try:
            self.serial.write(buf.encode('utf-8'))
            return True
        except SerialException:
            raise

    def read_lines(self):
        res = self.serial.read(50)
        if len(res):
            return res.splitlines()
        else:
            return []
