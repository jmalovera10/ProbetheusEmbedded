import time

from .. import sensor_manager

if __name__ == '__main__':
    manager = sensor_manager.SensorManager()
    try:
        while True:
            print('pH: ', manager.process_ph_measurement())
            time.sleep(1)
            print('CONDUCTIVITY: ', manager.process_conductivity_measurement())
            time.sleep(1)
            print('TURBIDITY: ', manager.process_turbidity_measurement())
            time.sleep(1)
    except KeyboardInterrupt:
        print('Finished')
