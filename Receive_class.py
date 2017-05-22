import serial
import sys
import glob


class Receiver:

    def __init__(self, dev_id):
        self.device_id = dev_id
        self.ser = serial.Serial()
        self.blue_channel = []
        self.green_channel = []
        self.number_of_elts = 0
        return

    def init_port(self):
        self.ser.baudrate = 115200
        self.ser.timeout = 1
        self.ser.parity = serial.PARITY_NONE
        self.ser.rtscts = 0
        ports_list = self.get_list_of_com_ports()
        if self.find_port(ports_list):
            return 1
        else:
            return 0
    def init_port_manually(self,port_name):
        self.ser.baudrate = 115200
        self.ser.timeout = 1
        self.ser.parity = serial.PARITY_NONE
        self.ser.rtscts = 0
        self.ser.port = port_name
        try:
            self.ser.open()
        except serial.SerialException as e:
            raise e


    def get_list_of_com_ports(self):
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            return 0

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        print(result)
        return result

    def find_port(self, port_list):
        for port in port_list:
            self.ser.port = port
            try:
                self.ser.open()
                self.ser.write(b'A')
                self.ser.write(b'\rL1\r')
                s = self.ser.read(5)
                if s != "pulse":
                    self.ser.close()
                else:
                    return 0
            except serial.SerialException as e:
                raise e
            return 1


    def send_request(self, data):
        try:
            self.ser.write(data)
        except serial.SerialException as e:
            raise e

        return

    def read_data(self):
        s = self.ser.read(7)
        self.parse_data(s)
        return


    def parse_data(self, parcel):
        if type(parcel) != type (b'as'):
            return 1
        if len(parcel) != 7:
            return 1

        try:
            parcel_str = parcel.decode('utf-8')
            blue = parcel_str[0:-4]
            green = parcel_str[3:-1]
            blue_int = int(blue, 16)
            green_int = int(green, 16)
            self.blue_channel.append(blue_int)
            self.green_channel.append(green_int)
            self.number_of_elts += 1
        except UnicodeEncodeError as e:
            raise e
            return 1
        except ValueError as e:
            raise e
            return 1
        return 0

    def full_read_procedure(self):
        self.send_request(b'\rL1\r')
        self.read_data()

    def clear_containers(self):
        self.blue_channel.clear()
        self.green_channel.clear()
        self.number_of_elts = 0

