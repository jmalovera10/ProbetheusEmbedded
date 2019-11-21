import RPi.GPIO as GPIO


class IndicatorManager:
    def __init__(self):
        self.active_indicator = True
        self.low_battery_indicator = False

        # Configure the setup for the pins
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(16, GPIO.OUT)
        GPIO.setup(20, GPIO.OUT)

    def set_active_indicator(self, new_state):
        self.active_indicator = new_state
        if new_state:
            GPIO.output(16, GPIO.HIGH)
        else:
            GPIO.output(16, GPIO.LOW)

    def set_low_battery_indicator(self, new_state):
        self.low_battery_indicator = new_state
        if new_state:
            GPIO.output(20, GPIO.HIGH)
        else:
            GPIO.output(20, GPIO.LOW)
