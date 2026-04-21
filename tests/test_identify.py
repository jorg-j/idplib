import os.path as path
import sys
import unittest
from unittest.mock import ANY
from idplib import ValueUtils

class test_identify_values(unittest.TestCase):
    def test_identify_creditcard(self):

        result = ValueUtils.Identify.credit_card_number('79927398713')

        self.assertEqual(result, True)

    def test_identify_invalid_creditcard(self):

        result = ValueUtils.Identify.credit_card_number('111111111111')

        self.assertEqual(result, False)


    def test_identify_abn(self):

        result = ValueUtils.Identify.abn('51 824 753 556')

        self.assertEqual(result, True)

    def test_identify_invalid_abn(self):

        result = ValueUtils.Identify.abn('111111111111')

        self.assertEqual(result, False)



if __name__ == '__main__':
    unittest.main()