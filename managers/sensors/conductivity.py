import serial
from serial import SerialException


class ConductivityManager:

    def __init__(self):
        try:
            self.serial = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1)
            self.wakeup_device()
            self.send_command('K,1')
            self.serial.flush()
        except SerialException as e:
            print("Error, ", e)

    def begin_continuous_readings(self):
        try:
            self.send_command('C,1')
            self.serial.flush()
            return True
        except SerialException as e:
            print ("Error, ", e)
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
            print ("Error, ", e)
            return None

    def sleep_device(self):
        try:
            self.send_command('Sleep')
            self.serial.flush()
            return True
        except SerialException as e:
            print ("Error, ", e)
            return None

    def wakeup_device(self):
        try:
            self.send_command('i')
            self.serial.flush()
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

    def read_line(self):
        lsl = len('\r')
        line_buffer = []
        while True:
            next_char = self.serial.read(1)
            if next_char == '':
                break
            line_buffer.append(next_char)
            if (len(line_buffer) >= lsl and
                    line_buffer[-lsl:] == list('\r')):
                break
        return ''.join(line_buffer)

    def read_lines(self):
        lines = []
        try:
            while True:
                line = self.read_line()
                if not line:
                    self.serial.flushInput()
                    break
                lines.append(line)
            return lines

        except SerialException as e:
            print("Error, ", e)
            return None
