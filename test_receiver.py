import unittest
from Receive_class import Receiver



class TestReceiver(unittest.TestCase):

    def test_parce_data(self):
        rec=Receiver()

        self.assertEqual(rec.parce_data(b'asdasd'),1,"fucked")
        self.assertEqual(rec.parce_data('Hello'), 1, "fucked")
        self.assertEqual(rec.parce_data(100), 1, "fucked")
        self.assertEqual(rec.parce_data(['a', 's', 'd']), 1, "fucked")



if __name__ == '__main__':
    unittest.main()