import os
import subprocess
import select
import serial
import time
import json
import re

wpa_supplicant_conf = "/etc/wpa_supplicant/wpa_supplicant.conf"
sudo_mode = "sudo "


class SerialComm:
    def __init__(self):
        self.port = serial.Serial("/dev/rfcomm0", baudrate=9600, timeout=1)

    def read_serial(self):
        res = self.port.read(50)
        if len(res):
            return res.splitlines()
        else:
            return []

    def send_serial(self, text):
        self.port.write(text)

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

    def isValidCommand(self, command, invalidCommand):
        if command not in invalidCommand:
            if re.match("^[a-zA-Z0-9. -]+$", command):
                return True

        return False

    def readExecuteSend(self, ble_line):
        json_object = json.loads(ble_line)
        return True


def main():
    shell = ShellWrapper()
    invalidCommand = ['clear', 'head', 'sudo', 'nano', 'touch', 'vim']
    ble_comm = None
    isConnected = False

    while True:
        try:
            ble_comm = SerialComm()
            out = ble_comm.read_serial()
            for ble_line in out:
                print(out)
                if ble_comm.is_json(ble_line):

                    if not isConnected:
                        isConnected = ble_comm.readExecuteSend(ble_line)
                        break
                    else:
                        ble_comm.send_serial("Wifi has been configured")
                        break

                if ble_comm.isValidCommand(ble_line, invalidCommand):

                    shell.execute_command(ble_line)
                    shell_out = shell.get_output()
                    if shell_out is not None:
                        for l in shell_out:
                            print(l)
                            ble_comm.send_serial(l)
                    else:
                        ble_comm.send_serial(
                            "command '" + ble_line + "' return nothing ")
                else:
                    ble_comm.send_serial(
                        "command '" + ble_line + "' not support ")

        except serial.SerialException:
            print("waiting for connection")
            ble_comm = None
            isConnected = False
            time.sleep(1)


if __name__ == "__main__":
    main()
