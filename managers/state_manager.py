class StateManager:
    def __init__(self, sensor_manager):
        self.state = "IDLE"
        self.sensor_manager = sensor_manager

    def change_state(self, new_state):
        self.state = new_state

    def manage(self, command, ble_comm):
        if self.state == "MEASURE":
            if command == "PH":
                print("PH SENT")
                self.sensor_manager.process_ph_measurement()
                ble_comm.send_serial('{"NAME":"PH","VALUE":6,"UNITS":""}')
            elif command == "CONDUCTIVIDAD":
                print("CONDUCTIVITY SENT")
                self.sensor_manager.process_conductivity_measurement()
                ble_comm.send_serial('{"NAME":"CONDUCTIVIDAD","VALUE":100,"UNITS":"uS/cm"}')
            elif command == "TURBIDEZ":
                print("TURBIDITY SENT")
                self.sensor_manager.process_turbidity_measurement()
                ble_comm.send_serial('{"NAME":"TURBIDEZ","VALUE":2,"UNITS":"FTU"}')
            elif command == "BATTERY":
                print("BATTERY STATUS SENT")
                ble_comm.send_serial('{"NAME":"BATTERY","VALUE":100,"UNITS":"%"}')
            '''
            elif command == "COLOR APARENTE":
                print("APPARENT_COLOR SENT")
                ble_comm.send_serial('{"NAME":"COLOR APARENTE","VALUE":10,"UNITS":"UPC"}')
            '''
