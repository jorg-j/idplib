import os.path as path
import sys
import unittest
from unittest.mock import ANY
from idplib import ValueUtils

class test_compare_values(unittest.TestCase):
    def test_compare_digits(self):

        result = ValueUtils.Compare.digits('$5', '$5,')

        self.assertEqual(result, True)

    def test_compare_strings(self):

        result = ValueUtils.Compare.string('the quick brown fox', 'the quick brown f0x')
        self.assertEqual(result, True)

    def test_compare_strings_neg(self):
        result = ValueUtils.Compare.string('slow yellow beans', 'the quick brown fox')
        self.assertEqual(result, False)       

    def test_compare_strings_manual_threshold(self):
        result = ValueUtils.Compare.string('the quick brown fox', 'the quick yellow f0x', threshold=99)
        self.assertEqual(result, False)

    def test_compare_strings_ignore_order(self):
        result = ValueUtils.Compare.string('the quick brown fox', 'brown quick the fox', ignore_order=True, token_ratio=89)
        self.assertEqual(result, True)

if __name__ == '__main__':
    unittest.main()