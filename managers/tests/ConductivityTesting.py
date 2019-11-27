from ..sensors import conductivity

if __name__ == '__main__':
    real_raw_input = vars(__builtins__).get('raw_input', input)  # used to find the correct function for python2/3

    print("\nWelcome to the Atlas Scientific Raspberry Pi UART example.\n")
    print("    Any commands entered are passed to the board via UART except:")
    print("    Poll,xx.x command continuously polls the board every xx.x seconds")
    print("    Pressing ctrl-c will stop the polling\n")
    print("    Press enter to receive all data in buffer (for continuous mode) \n")

    # to get a list of ports use the command:
    # python -m serial.tools.list_ports
    # in the terminal

    manager = conductivity.ConductivityManager()
    try:
        while True:
            input_val = real_raw_input("Enter command: ")
            manager.send_command(input_val)
            print('CONDUCTIVITY: ', manager.read_lines())
    except KeyboardInterrupt:
        print('Finished')
