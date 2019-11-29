import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import RPi.GPIO as GPIO


class TurbidityManager:

    def __init__(self):
        # Create the I2C bus
        i2c = busio.I2C(board.SCL, board.SDA)
        # Create the ADC object using the I2C bus
        ads = ADS.ADS1115(i2c)
        # Create single-ended input on channel 1 for turbidity
        self.turbidity_angle1 = AnalogIn(ads, ADS.P1)
        self.turbidity_angle2 = AnalogIn(ads, ADS.P2)
        self.turbidity_value = None

        # Configure infrared LED outputs
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        # A1- GPIO 27 pairing
        GPIO.setup(27, GPIO.OUT)
        GPIO.output(27, GPIO.LOW)
        # A2- GPIO 17 pairing
        GPIO.setup(17, GPIO.OUT)
        GPIO.output(17, GPIO.LOW)

    def get_turbidity_measurement(self):
        turbidity_angle1 = 0
        turbidity_angle2 = 0
        for i in range(10):
            # First perspective measurement
            GPIO.output(27, GPIO.HIGH)
            voltage_angle1 = self.turbidity_angle1.voltage
            turbidity_angle1 += (-594.887612 * voltage_angle1) + 2525.903701
            GPIO.output(27, GPIO.LOW)
            # Second perspective measurement
            GPIO.output(17, GPIO.HIGH)
            voltage_angle2 = self.turbidity_angle2.voltage
            turbidity_angle2 += (-594.887612 * voltage_angle2) + 2525.903701
            GPIO.output(17, GPIO.LOW)
        self.turbidity_value = (turbidity_angle1 + turbidity_angle2) / 20
        return self.turbidity_value, "NTU"
