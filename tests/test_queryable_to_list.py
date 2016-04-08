import unittest
import pinq


class queryable_to_list_tests(unittest.TestCase):

    def setUp(self):
        self.queryable = pinq.as_queryable(range(1, 11))

    def test_to_list(self):
        self.assertEqual(self.queryable.to_list(), [
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
