from managers.sensors.conductivity import ConductivityManager
from managers.sensors.pH import pHManager
from managers.sensors.turbidity import TurbidityManager


class SensorManager:
    def __init__(self):
        pass

    @staticmethod
    def process_ph_measurement():
        ph = pHManager()
        return ph.get_ph_measurement()

    @staticmethod
    def process_conductivity_measurement():
        conductivity = ConductivityManager()
        reading = conductivity.make_reading()
        conductivity.sleep_device()
        return reading

    @staticmethod
    def process_turbidity_measurement():
        turbidity = TurbidityManager()
        return turbidity.get_turbidity_measurement()
