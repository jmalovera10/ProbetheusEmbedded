import json
import time
import threading

import serial
from bluetooth import *

from managers.indicator_manager import IndicatorManager
from managers.state_manager import StateManager


def is_json(mJson):
    try:
        json_object = json.loads(mJson)
        if isinstance(json_object, int):
            return False

        if len(json_object) == 0:
            return False

    except ValueError:
        return False
    return True


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


class StateThread(threading.Thread):
    def __init__(self, state_manager):
        threading.Thread.__init__(self)
        self.state_manager = state_manager
        self.ble_comm = None
        self.lock = threading.Lock()

    def set_ble_comm(self, ble_comm):
        self.ble_comm = ble_comm

    def change_state(self, state, command):
        self.lock.acquire()
        self.state_manager.change_state(state, command)
        self.lock.release()

    def run(self):
        while True:
            self.lock.acquire()
            self.state_manager.manage(self.ble_comm)
            self.lock.release()
            time.sleep(0.1)


def main():
    # Setup BT
    # le_comm = SerialComm()
    server_sock = BluetoothSocket(RFCOMM)
    server_sock.bind(("", PORT_ANY))
    server_sock.listen(1)

    port = server_sock.getsockname()[1]

    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

    advertise_service(server_sock, "SampleServer",
                      service_id=uuid,
                      service_classes=[uuid, SERIAL_PORT_CLASS],
                      profiles=[SERIAL_PORT_PROFILE],
                      #                   protocols = [ OBEX_UUID ]
                      )

    print("Waiting for connection on RFCOMM channel %d" % port)

    # Setup managers
    indicator_manager = IndicatorManager()
    indicator_manager.set_low_battery_indicator(False)
    state_manager = StateManager(indicator_manager)

    state_thread = StateThread(state_manager)
    state_thread.start()
    client_sock, client_info = server_sock.accept()
    indicator_manager.set_active_indicator(True)
    state_thread.set_ble_comm(client_sock)

    while True:
        try:
            # out = ble_comm.read_serial()
            data = client_sock.recv(1024)
            if len(data) == 0:
                raise btcommon.BluetoothError
            print('INCOMING RAW DATA: ', data)
            if is_json(data):
                print(data)
                message = json.loads(data)
                state = message['STATE']
                command = message['COMMAND']
                state_thread.change_state(state, command)
            '''
            for ble_line in out:
                print(out)
                if ble_comm.is_json(ble_line):
                    message = json.loads(ble_line)
                    state = message['STATE']
                    command = message['COMMAND']
                    state_thread.change_state(state, command)
            '''

        except serial.SerialException:
            print("waiting for connection")
            time.sleep(0.5)
        except btcommon.BluetoothError:
            print('CONNECTION TERMINATED')
            indicator_manager.set_active_indicator(False)
            client_sock, client_info = server_sock.accept()
            state_thread.set_ble_comm(client_sock)
            indicator_manager.set_active_indicator(True)
        except KeyError:
            print('BAD REQUEST')


if __name__ == "__main__":
    main()
