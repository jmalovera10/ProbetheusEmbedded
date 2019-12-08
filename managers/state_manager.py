from . import sensor_manager, battery_manager


class StateManager:
    def __init__(self, indicator_manager):
        self.state = "IDLE"
        self.command = "EMPTY"
        self.sensor_manager = sensor_manager.SensorManager()
        self.battery_manager = battery_manager.BatteryManager(indicator_manager)

    def change_state(self, new_state, command):
        self.state = new_state
        self.command = command

    def manage(self, ble_comm):
        if self.state == "MEASURE":
            if self.command == "pH":
                print("PH SENT")
                ph = self.sensor_manager.process_ph_measurement()
                # ble_comm.send_serial('{"NAME":"pH","VALUE":%.3f,"UNITS":"%s"}' % (ph[0], ph[1]))
                ble_comm.send('{"NAME":"pH","VALUE":%.3f,"UNITS":"%s"}' % (ph[0], ph[1]))
            elif self.command == "CONDUCTIVIDAD":
                print("CONDUCTIVITY SENT")
                conductivity = self.sensor_manager.process_conductivity_measurement()
                #ble_comm.send_serial(
                    #'{"NAME":"CONDUCTIVIDAD","VALUE":%.3f,"UNITS":"%s"}' % (conductivity[0], conductivity[1]))
                ble_comm.send('{"NAME":"CONDUCTIVIDAD","VALUE":%.3f,"UNITS":"%s"}' % (conductivity[0], conductivity[1]))
            elif self.command == "TURBIEDAD":
                print("TURBIDITY SENT")
                turbidity = self.sensor_manager.process_turbidity_measurement()
                # ble_comm.send_serial('{"NAME":"TURBIEDAD","VALUE":%.3f,"UNITS":"%s"}' % (turbidity[0], turbidity[1]))
                ble_comm.send('{"NAME":"TURBIEDAD","VALUE":%.3f,"UNITS":"%s"}' % (turbidity[0], turbidity[1]))
            elif self.command == "BATTERY":
                print("BATTERY STATUS SENT")
                battery = self.battery_manager.get_battery_measurement()
                #ble_comm.send_serial('{"NAME":"BATTERY","VALUE":%d,"UNITS":"%s"}' % (battery[0], battery[1]))
                ble_comm.send('{"NAME":"BATTERY","VALUE":%d,"UNITS":"%s"}' % (battery[0], battery[1]))
