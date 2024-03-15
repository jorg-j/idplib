import os.path as path
import sys
import unittest
from unittest.mock import ANY
from IDPlib import ValueUtils
import datetime

class test_normalised_values(unittest.TestCase):
    def test_1_1(self):

        result = ValueUtils.Normalise.digit('$5')

        self.assertEqual(result, '5')

    
    def test_1_2(self):

        result = ValueUtils.Normalise.digit('$5a')

        self.assertNotEqual(result, '5')

    def test_safe_round(self):

        result = ValueUtils.Normalise.safe_round(1.5)
        self.assertEqual(result, 1.5)
  
        result = ValueUtils.Normalise.safe_round(1.50000000000000001)
        self.assertEqual(result, 1.5)

        result = ValueUtils.Normalise.safe_round(1.515)
        self.assertEqual(result, 1.52)


    def test_date_convert_fromstring(self):
        result = ValueUtils.Normalise.Date.from_string('1/5/2024')
        expects = datetime.datetime(2024, 5,1, 0, 0)
        self.assertEqual(result, expects)


    def test_date_trax_year(self):
        result = ValueUtils.Normalise.Date.tax_year('1/5/2024')

        self.assertEqual(result, 2024)

        result = ValueUtils.Normalise.Date.tax_year('1/8/2024')

        self.assertEqual(result, 2025)

if __name__ == '__main__':
    unittest.main()