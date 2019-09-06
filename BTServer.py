import os
import subprocess
import select
import serial
import time
import json
import re
import random


class SerialComm:
    def __init__(self):
        self.port = serial.Serial("/dev/rfcomm0", baudrate=9600, timeout=1)

    def read_serial(self):
        return self.port.readline()

    def send_serial(self, text):
        self.port.write(text + str('\n'))


def main():
    ble_comm = None

    while True:
        try:
            ble_comm = SerialComm()
            out = ble_comm.read_serial()
            for ble_line in out:
                print(out)
                ble_comm.send_serial(ble_line)

        except serial.SerialException:
            print("waiting for connection")
            ble_comm = None
            time.sleep(1)


if __name__ == "__main__":
    main()
