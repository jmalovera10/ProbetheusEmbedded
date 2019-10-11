import os
import subprocess
import select
import serial
import time
import json
import re
import random
import RPi.GPIO as GPIO


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
                ble_comm.send_serial('{"NAME":"PH","VALUE":6,"UNITS":""}')
            elif command == "CONDUCTIVIDAD":
                print("CONDUCTIVITY SENT")
                ble_comm.send_serial('{"NAME":"CONDUCTIVIDAD","VALUE":100,"UNITS":"uS/cm"}')
            elif command == "TURBIDEZ":
                print("TURBIDITY SENT")
                ble_comm.send_serial('{"NAME":"TURBIDEZ","VALUE":2,"UNITS":"FTU"}')
            elif command == "COLOR APARENTE":
                print("APPARENT_COLOR SENT")
                ble_comm.send_serial('{"NAME":"COLOR APARENTE","VALUE":10,"UNITS":"UPC"}')
            elif command == "BATTERY":
                print("BATTERY STATUS SENT")
                ble_comm.send_serial('{"NAME":"BATTERY","VALUE":100,"UNITS":"%"}')

class SensorManager:
    def __init__(self):
        self.active_indicator = True


class IndicatorManager:
    def __init__(self):
        self.active_indicator = True
        self.low_battery_indicator = False

        # Configure the setup for the pins
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(16,GPIO.OUT)
        GPIO.setup(20,GPIO.OUT)

        # Output the default values for the indicators
        GPIO.output(16, GPIO.HIGH)
        GPIO.output(20, GPIO.LOW)

    
    def set_active_indicator(self, new_state):
        self.active_indicator = new_state
        if new_state:
            GPIO.output(16, GPIO.HIGH)
        else:
            GPIO.output(16, GPIO.LOW)

    def set_low_battery_indicator(self, new_state):
        self.low_battery_indicator = new_state
        if new_state:
            GPIO.output(20, GPIO.HIGH)
        else:
            GPIO.output(20, GPIO.LOW)


def main():
    ble_comm = None
    state_manager = StateManager()
    indicator_manager = IndicatorManager()

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
                    state_manager.change_state(state)
                    state_manager.manage(command, ble_comm)

        except serial.SerialException:
            print("waiting for connection")
            ble_comm = None
            time.sleep(1)


if __name__ == "__main__":
    main()
