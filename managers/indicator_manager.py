import RPi.GPIO as GPIO


class IndicatorManager:
    def __init__(self):
        self.active_indicator = True
        self.low_battery_indicator = False

        # Configure the setup for the pins
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        return
        # Active LED
        GPIO.setup(18, GPIO.OUT)
        # Battery LED
        GPIO.setup(23, GPIO.OUT)

    def set_active_indicator(self, new_state):
        return
        self.active_indicator = new_state
        if new_state:
            GPIO.output(18, GPIO.HIGH)
        else:
            GPIO.output(18, GPIO.LOW)

    def set_low_battery_indicator(self, new_state):
        return
        self.low_battery_indicator = new_state
        if new_state:
            GPIO.output(23, GPIO.HIGH)
        else:
            GPIO.output(23, GPIO.LOW)
