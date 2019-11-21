import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from conductivity import ConductivityManager


class SensorManager:
    def __init__(self):
        # Create the I2C bus
        i2c = busio.I2C(board.SCL, board.SDA)
        # Create the ADC object using the I2C bus
        ads = ADS.ADS1115(i2c)
        # Create single-ended input on channel 0 for pH
        self.pHSensor = AnalogIn(ads, ADS.P0)
        # Create single-ended input on channel 1 for battery
        self.battery = AnalogIn(ads, ADS.P1)
        # Create single-ended input on channel 1 for turbidity
        self.turbidity = AnalogIn(ads, ADS.P2)

    def process_ph_measurement(self):
        voltage = self.pHSensor.voltage
        ph_value = (-5.6548 * voltage) + 15.509
        return ph_value, ""

    @staticmethod
    def process_conductivity_measurement():
        conductivity = ConductivityManager()
        reading = conductivity.make_reading()
        print reading
        return reading

    # def process_apparent_color_measurement(self):
    # return False

    def process_turbidity_measurement(self):
        voltage = self.turbidity.voltage
        turbidity = voltage * 10
        return turbidity
