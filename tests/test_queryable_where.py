import unittest
import pinq


class queryable_where_tests(unittest.TestCase):

    def setUp(self):
        self.queryable = pinq.as_queryable(range(1, 11))

    def test_where_all(self):
        self.assertEqual(list(self.queryable.where(lambda x: x > 0)), [
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    def test_where_some(self):
        self.assertEqual(list(self.queryable.where(
            lambda x: x < 6)), [1, 2, 3, 4, 5])

    def test_where_none(self):
        self.assertEqual(list(self.queryable.where(lambda x: x > 100)), [])

    def test_where_all_with_index(self):
        self.assertEqual(list(self.queryable.where(lambda x, y: y < 10)), [
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    def test_where_some_with_index(self):
        self.assertEqual(list(self.queryable.where(
            lambda x, y: y % 2 == 0)), [1, 3, 5, 7, 9])

    def test_where_none_with_index(self):
        self.assertEqual(list(self.queryable.where(lambda x, y: y > 100)), [])

    def test_where_predicate_type_error(self):
        self.assertRaises(TypeError, self.queryable.where, 100)
