from . import sensor_manager, battery_manager


class StateManager:
    def __init__(self):
        self.state = "IDLE"
        self.sensor_manager = sensor_manager.SensorManager()
        self.battery_manager = battery_manager.BatteryManager()

    def change_state(self, new_state):
        self.state = new_state

    def manage(self, command, ble_comm):
        if self.state == "MEASURE":
            if command == "PH":
                print("PH SENT")
                ph = self.sensor_manager.process_ph_measurement()
                ble_comm.send_serial('{"NAME":"PH","VALUE":%.8f,"UNITS":"%s"}' % (ph[0], ph[1]))
            elif command == "CONDUCTIVIDAD":
                print("CONDUCTIVITY SENT")
                conductivity = self.sensor_manager.process_conductivity_measurement()
                ble_comm.send_serial(
                    '{"NAME":"CONDUCTIVIDAD","VALUE":%.8f,"UNITS":"%s"}' % (conductivity[0], conductivity[1]))
            elif command == "TURBIDEZ":
                print("TURBIDITY SENT")
                turbidity = self.sensor_manager.process_turbidity_measurement()
                ble_comm.send_serial('{"NAME":"TURBIDEZ","VALUE":%.8f,"UNITS":"%s"}' % (turbidity[0], turbidity[1]))
            elif command == "BATTERY":
                print("BATTERY STATUS SENT")
                battery = self.battery_manager.get_battery_measurement()
                ble_comm.send_serial('{"NAME":"BATTERY","VALUE":%d,"UNITS":"%s"}' % (battery[0], battery[1]))
