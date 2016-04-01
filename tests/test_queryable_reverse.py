import unittest
import pinq


class queryable_reverse_tests(unittest.TestCase):

    def setUp(self):
        self.queryable = pinq.as_queryable(
            [1, 2, 3.0, "apple", "banana", [2.1, 16], 0])

    def test_of_type_str(self):
        self.assertEqual(list(self.queryable.reverse()), [
            0, [2.1, 16], "banana", "apple", 3.0, 2, 1])
