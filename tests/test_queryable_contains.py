import unittest
import pinq


class queryable_contains_tests(unittest.TestCase):

    def setUp(self):
        self.queryable = pinq.as_queryable([1, 1, 2, 3, 4, 5, 6, 6, 7, 8])

    def test_contains_single(self):
        self.assertEqual(self.queryable.contains(5), True)

    def test_contains_multiple(self):
        self.assertEqual(self.queryable.contains(6), True)

    def test_contains_none(self):
        self.assertEqual(self.queryable.contains(10), False)

    def test_contains_custom_comparer_single(self):
        self.assertEqual(self.queryable.contains(
            6, lambda x, y: x - 4 == y), True)

    def test_contains_custom_comparer_multiple(self):
        self.assertEqual(self.queryable.contains(
            10, lambda x, y: x - 4 == y), True)

    def test_contains_custom_comparer_none(self):
        self.assertEqual(self.queryable.contains(
            1, lambda x, y: x - 4 == y), False)

    def test_contains_equality_comparer_type_error(self):
        self.assertRaises(TypeError, self.queryable.contains, 12, 100)
