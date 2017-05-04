import matplotlib.pyplot as plt
from numpy.fft import rfft
from scipy import signal


class PlottingError(BaseException):
    def __init__(self, error):
        self.error_description = error

    def what(self):
        return self.error_description


def get_signal(filename: str):
    signal_file = open(filename, 'r')
    signal = []
    for line in signal_file:
        signal.append(int(line))

    signal_file.close()
    return signal


class SignalFilter:
    def __init__(self, signal, necessary_length):
        if len(signal) < necessary_length:
            print('You\'ve made a mistake in initialization of the necessary_length parameter,',
                  'so, be default the necessary_length = len(your_signal).')
            necessary_length = len(signal)
        self.raw_signal = signal[0:necessary_length]
        self.filtered_signal = [0, ]

    def plot(self):
        plt.plot(self.raw_signal, 'r')
        plt.plot(self.filtered_signal, 'g', linewidth=2.0)
        plt.xlabel('Номера отсчета')
        plt.ylabel('Значение')
        plt.title('Сравнение исходного и отфильтрованного сигналов')
        plt.grid(True)
        plt.show()

    def forward_backward_filter(self):
        # возвращает числитель и знаменатель полинома бесконечной импульстной характеристики
        b, a = signal.butter(5, 0.125)
        # алгоритм прямого-обратного хода - используется для действий с последовательностями,
        # внутри которых содержатся зашумленные результаты
        self.filtered_signal = signal.filtfilt(b, a, self.raw_signal[:])


class FourierTransformaion:
    def __init__(self, input_signal):
        self.signal = input_signal

    def _make_spectrum_Re(self):
        Re_spectrum = []
        for i in self.spectrum:
            i = abs(i)
            Re_spectrum.append(i)

        Re_spectrum = Re_spectrum[1:]
        self.spectrum = Re_spectrum[:]

    def plot(self, signal_name):
        # try:
            if signal_name == 'signal':
                plt.plot(self.signal, 'r')
                plt.xlabel('Измерения')
                plt.ylabel('Значение')
                plt.title('Пришедший сигнал')
            elif signal_name == 'full spectrum' or signal_name == 'cut spectrum':
                plt.xlabel('Номера измерений')
                plt.ylabel('Значение частоты')
                plt.title('Спектр')
                if signal_name == 'cut spectrum':
                    plt.xlim(xmax=50)

                plt.plot(self.spectrum)
                plt.title('spectrum1')
            else:
                raise PlottingError('you can plot signal or spectrum and nothing else')
            plt.grid(True)
            plt.show()
        # except PlottingError as e:
        #     print(e.what())

    def transform(self):
        self.spectrum = rfft(self.signal)
        self._make_spectrum_Re()

        
def cut_min(array):
    j = 0
    x1 = array[j]
    x2 = array[j]
    while x2 >= x1:
        x1 = x2
        j += 1
        x2 = array[j]
    while x2 <= x1:
        x1 = x2
        j += 1
        x2 = array[j]

    return j


class Heart_rate_calculator:
    def __init__(self, spectrum):
        self.spectrum = spectrum[3:]
        self.result = []

    def _get_two_high_points(self):
        dict_spectrum = {}
        for i in range(len(self.spectrum)):
            dict_spectrum[int(self.spectrum[i])] = i

        array_cpy = self.spectrum
        extremums = []
        j = 0
        for i in range(2):
            j += cut_min(array_cpy)
            array_cpy = array_cpy[j:]
            sorted_cpy = array_cpy[:]
            sorted_cpy.sort()
            extremums.append(sorted_cpy[-1])

        result = []
        result.append(dict_spectrum[int(extremums[0])])
        result.append(dict_spectrum[int(extremums[1])])

        return result

    def calculate_results(self):
        array = [16, 14, 12, 10, 5, 6, 8, 9, 3, 2, 5, 0, 1]
        self.result = self._get_two_high_points()


if __name__ == "__main__":

    raw_signal = get_signal('raw_signal.txt')
    flt = SignalFilter(raw_signal, 2048)
    flt.forward_backward_filter()
    flt.plot()

    ft = FourierTransformaion(flt.filtered_signal)
    ft.transform()
    ft.plot('full spectrum')
    ft.plot('cut spectrum')

    clcltr = Heart_rate_calculator(ft.spectrum)
    clcltr.calculate_results()
    print(clcltr.result)

