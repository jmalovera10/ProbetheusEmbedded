import time

from .. import battery_manager

if __name__ == '__main__':
    manager = battery_manager.BatteryManager()
    try:
        while True:
            print('BATTERY LEVEL: ', manager.get_battery_measurement())
            time.sleep(2)
    except KeyboardInterrupt:
        print('Finished')
