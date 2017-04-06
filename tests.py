import unittest
import signal_processing as sp


class PlotTest(unittest.TestCase):

    def test_plot(self):
        '''при ошибочном указании желаемого графика - возникает исключение'''
        raw_signal = sp.get_signal('raw_signal.txt')
        filt = sp.SignalFilter(raw_signal, 2048)
        filt.forward_backward_filter()

        ft = sp.FourierTransformaion(filt.filtered_signal)
        ft.transform()

        with self.assertRaises(sp.PlottingError):
            ft.plot('cuttttt spectrum')

if __name__ == '__main__':
    unittest.main()
