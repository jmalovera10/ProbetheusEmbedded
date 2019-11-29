import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


class pHManager:

    def __init__(self):
        # Create the I2C bus
        i2c = busio.I2C(board.SCL, board.SDA)
        # Create the ADC object using the I2C bus
        ads = ADS.ADS1115(i2c)
        # Create single-ended input on channel 0 for pH
        self.pHSensor = AnalogIn(ads, ADS.P3)
        self.pH_value = None

    def get_ph_measurement(self):
        self.pH_value = 0
        for i in range(10):
           voltage = self.pHSensor.voltage
           self.pH_value += (-5.6548 * voltage) + 15.509
        self.pH_value /= 10
        return self.pH_value, ""
