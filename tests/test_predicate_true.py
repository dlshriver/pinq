import unittest
from pinq.predicates import true


class predicate_true_tests(unittest.TestCase):

    def test_true_int(self):
        self.assertEqual(true(123), True)

    def test_true_str(self):
        self.assertEqual(true("apple"), True)

    def test_true_list(self):
        self.assertEqual(true(["great", 100029]), True)
