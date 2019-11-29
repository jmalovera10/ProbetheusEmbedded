import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


class BatteryManager:
    def __init__(self):
        # Create the I2C bus
        i2c = busio.I2C(board.SCL, board.SDA)
        # Create the ADC object using the I2C bus
        ads = ADS.ADS1115(i2c)
        # Create single-ended input on channel 1 for battery
        self.battery = AnalogIn(ads, ADS.P0)
        self.battery_value = None

    def get_battery_measurement(self):
        voltage = self.battery.voltage
        print(voltage)
        self.battery_value = ((voltage - 2.8) * 100.0) / 1.4
        return self.battery_value, "%"
