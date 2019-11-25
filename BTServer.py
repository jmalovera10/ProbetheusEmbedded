import json
import time
import threading

import serial

from managers.indicator_manager import IndicatorManager
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
        value = (text + str('\r\n')).encode()
        self.port.write(value)

    def is_json(self, mJson):
        try:
            json_object = json.loads(mJson)
            if isinstance(json_object, int):
                return False

            if len(json_object) == 0:
                return False

        except ValueError:
            return False
        return True


class StateThread(threading.Thread):
    def __init__(self, state_manager, ble_comm):
        threading.Thread.__init__(self)
        self.state_manager = state_manager
        self.ble_comm = ble_comm
        self.lock = threading.Lock()

    def change_state(self, state, command):
        self.lock.acquire()
        self.state_manager.change_state(state, command)
        self.lock.release()

    def run(self):
        while True:
            self.state_manager.manage(self.ble_comm, self.lock)
            time.sleep(0.1)


def main():
    ble_comm = SerialComm()
    # Setup managers
    state_manager = StateManager()
    indicator_manager = IndicatorManager()
    indicator_manager.set_active_indicator(True)
    indicator_manager.set_low_battery_indicator(False)

    state_thread = StateThread(state_manager,ble_comm)
    state_thread.start()

    while True:
        try:
            out = ble_comm.read_serial()
            for ble_line in out:
                print(out)
                if ble_comm.is_json(ble_line):
                    message = json.loads(ble_line)
                    state = message['STATE']
                    command = message['COMMAND']
                    state_thread.change_state(state, command)

        except serial.SerialException:
            print("waiting for connection")
            time.sleep(0.5)
        except KeyError:
            print('BAD REQUEST')


if __name__ == "__main__":
    main()
