import json
import time

import serial

from managers.indicator_manager import IndicatorManager
from managers.sensor_manager import SensorManager
from managers.state_manager import StateManager


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


def main():
    ble_comm = None
    # Setup managers
    sensor_manager = SensorManager()
    state_manager = StateManager(sensor_manager)
    indicator_manager = IndicatorManager()
    indicator_manager.set_active_indicator(True)
    indicator_manager.set_low_battery_indicator(False)

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
        except KeyError:
            print('BAD REQUEST')


if __name__ == "__main__":
    main()
