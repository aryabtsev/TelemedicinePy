
import serial


class Receiver:

    def __init__(self):
        self.ser = serial.Serial()
        self.blue_channel = []
        self.green_channel = []
        self.number_of_elts = 0
        return

    def init_port(self, com_port):
        self.ser.port = com_port
        self.ser.baudrate = 115200
        self.ser.timeout = 1
        self.ser.parity = serial.PARITY_NONE
        self.ser.rtscts = 0
        try:
            self.ser.open()
        except serial.SerialException:
            print("cant open port")
            return 0
        return 1

    def send_request(self):
        try:
            self.ser.write(b'\rL1\r')
        except serial.SerialException:
            print("port is not opened")

        return

    def read_data(self):
        s = self.ser.read(7)
        self.parce_data(s)
        return

    def say_hello(self):
        print("hello")

    def parce_data(self, parcel):
        if type(parcel) != type (b'as'):
            return 1
        if len(parcel) != 7:
            return 1
        try:
            parcel_str = parcel.decode('utf-8')
        except UnicodeEncodeError:
            print("broken Data")
            return 1

        blue = parcel_str[0:-4]
        try:
            blue_int = int(blue, 16)
        except ValueError:
            print("broken data")
            return 1

        green = parcel_str[3:-1]
        try:
            green_int = int(green, 16)
        except ValueError:
            print("broken data")
            return 1

        self.blue_channel.append(blue_int)
        self.green_channel.append(green_int)
        self.number_of_elts += 1
        return 0

rec = Receiver()

if rec.init_port('COM3') == 1:
    rec.send_request()
    rec.read_data()
 #   while rec.number_of_elts != 256:
  #      rec.send_request()
   #     rec.read_data()

print(rec.blue_channel)
