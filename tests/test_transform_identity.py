import unittest
from pinq.transforms import identity


class predicate_true_tests(unittest.TestCase):

    def test_identity_int(self):
        self.assertEqual(identity(123), 123)

    def test_identity_str(self):
        self.assertEqual(identity("apple"), "apple")

    def test_identity_list(self):
        self.assertEqual(identity(["great", 100029]), ["great", 100029])
