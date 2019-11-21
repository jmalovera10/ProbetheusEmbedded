import time

from .. import indicator_manager

if __name__ == '__main__':
    manager = indicator_manager.IndicatorManager()
    try:
        battery_indicator = True
        active_indicator = False
        while True:
            manager.set_low_battery_indicator(battery_indicator)
            print('BATTERY_INDICATOR: ', battery_indicator)
            battery_indicator = not active_indicator
            time.sleep(3)
            manager.set_active_indicator(active_indicator)
            active_indicator = not active_indicator
            print('ACTIVE_INDICATOR: ', active_indicator)
            time.sleep(3)
    except KeyboardInterrupt:
        print('Finished')
