import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


class BatteryManager:
    def __init__(self, indicator_manager):
        # Create the I2C bus
        i2c = busio.I2C(board.SCL, board.SDA)
        # Create the ADC object using the I2C bus
        ads = ADS.ADS1115(i2c)
        # Create single-ended input on channel 1 for battery
        self.battery = AnalogIn(ads, ADS.P0)
        self.battery_value = None
        self.indicator_manager = indicator_manager

    def get_battery_measurement(self):
        accumulator = 0
        for i in range(20):
            voltage = self.battery.voltage
            print(voltage)
            accumulator += ((voltage - 2.9) * 100.0) / (4.2 - 2.9)
        self.battery_value = accumulator / 20
        if self.battery_value < 20:
            self.indicator_manager.set_low_battery_indicator(True)
        else:
            self.indicator_manager.set_low_battery_indicator(False)
        return self.battery_value, "%"
