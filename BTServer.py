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
        # return self.port.readline()
        res = self.port.read(50)
        if len(res):
            return res.splitlines()
        else:
            return []

    def send_serial(self, text):
        self.port.write((text + str('\n')).encode())

    def is_json(self, mJson):
        try:
            json_object = json.loads(mJson)
            if isinstance(json_object, int):
                return False

            if len(json_object) == 0:
                return False

        except ValueError as e:
            return False
        return True


class StateManager:
    def __init__(self):
        self.state = "IDLE"

    def change_state(self, new_state):
        self.state = new_state

    def manage(self, command, ble_comm):
        if self.state == "MEASURE":
            if command == "PH":
                print("PH SENT")
                ble_comm.send_serial("PH MEASUREMENT")
            elif command == "DO":
                print("DO SENT")
                ble_comm.send_serial("DO MEASUREMENT")
            elif command == "T":
                print("T SENT")
                ble_comm.send_serial("T MEASUREMENT")
            elif command == "AC":
                print("AC SENT")
                ble_comm.send_serial("AC MEASUREMENT")


def main():
    ble_comm = None
    manager = StateManager()

    while True:
        try:
            ble_comm = SerialComm()
            out = ble_comm.read_serial()
            for ble_line in out:
                print(out)
                if ble_comm.is_json(ble_line):
                    message = json.loads(ble_line)
                    state = message['STATE']
                    command = message['COMMAND']
                    manager.change_state(state)
                    manager.manage(command, ble_comm)

        except serial.SerialException:
            print("waiting for connection")
            ble_comm = None
            time.sleep(1)


if __name__ == "__main__":
    main()
