import time

from managers.battery_manager import BatteryManager

if __name__ == '__main__':
    manager = BatteryManager()
    try:
        while True:
            print('BATTERY LEVEL: ', manager.get_battery_measurement())
            time.sleep(2)
    except KeyboardInterrupt:
        print('Finished')
