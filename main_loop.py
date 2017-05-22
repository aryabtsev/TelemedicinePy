import MySQLdb
import  time
import datetime

import serial
from signal_processing import Heart_rate_calculator
from signal_processing import SignalFilter
from signal_processing import FourierTransformaion
from Receive_class import  Receiver
from DBwriter_class import DbWriter


device = Receiver(1)
device.init_port_manually('COM5')
signal_size = 4096
t = 0.002

def full_signal_procedure(signal):
    flt = SignalFilter(signal, signal_size)
    flt.forward_backward_filter()

    ft = FourierTransformaion(flt.filtered_signal)
    ft.transform()

    clcltr = Heart_rate_calculator(ft.spectrum)
    heart_freq, breath_freq = clcltr.get_fft_maximums()
    heart_rate =60*1.57* heart_freq * 1/(signal_size*t)
    breath_rate = 60 * 1.57 * breath_freq * 1 / (signal_size * t)
    print(heart_rate, breath_rate)
    #ft.plot('cut spectrum')
    return heart_rate, breath_rate

try:
    writer = DbWriter("173.230.151.37", 3306, "root", "BMT4Ever", "mydb")
    writer.connect_to_db()

    while 1:
        device.full_read_procedure()
        if device.number_of_elts == signal_size:
            heart_rate, breath_rate = full_signal_procedure(device.blue_channel)
            print (heart_rate, breath_rate)
            date_now = time.strftime('%Y-%m-%d')
            time_now = time.strftime('%H:%M:%S')
            writer.push_to_db(heart_rate, breath_rate, device.device_id, date_now, time_now)
            device.clear_containers()


except serial.SerialException as e:
    print(e)
    pass
except UnicodeDecodeError as e:
    print(e)
    pass
except ValueError as e:
    print(e)
    pass
except MySQLdb.Error as e:
    print(e)