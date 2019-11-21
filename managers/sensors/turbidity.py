import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


class TurbidityManager:

    def __init__(self):
        # Create the I2C bus
        i2c = busio.I2C(board.SCL, board.SDA)
        # Create the ADC object using the I2C bus
        ads = ADS.ADS1115(i2c)
        # Create single-ended input on channel 1 for turbidity
        self.turbidity = AnalogIn(ads, ADS.P2)
        self.turbidity_value = None

    def get_turbidity_measurement(self):
        voltage = self.turbidity.voltage
        self.turbidity_value = (-5.6548 * voltage) + 15.509
        return self.turbidity_value, "NTU"
