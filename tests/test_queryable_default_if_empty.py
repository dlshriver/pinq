import unittest
import pinq


class queryable_default_if_empty_tests(unittest.TestCase):

    def setUp(self):
        self.queryable1 = pinq.as_queryable([])
        self.queryable2 = pinq.as_queryable(range(1, 6))

    def test_default_if_empty_non_empty(self):
        self.assertEqual(
            list(self.queryable2.default_if_empty()), [1, 2, 3, 4, 5])

    def test_default_if_empty_is_empty(self):
        self.assertEqual(list(self.queryable1.default_if_empty()), [None])

    def test_default_if_empty_is_empty_provide_value(self):
        self.assertEqual(list(self.queryable1.default_if_empty(0)), [0])
