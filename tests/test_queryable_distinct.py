import unittest
import pinq


class queryable_distinct_tests(unittest.TestCase):

    def setUp(self):
        self.queryable1 = pinq.as_queryable([])
        self.queryable2 = pinq.as_queryable([1, 2, 3, 4, 5])
        self.queryable3 = pinq.as_queryable([1, 2, 3, 1, 4, 5, 2, 5, 6])
        self.queryable4 = pinq.as_queryable([1, 1, 1, 1, 1])

    def test_distinct_empty(self):
        self.assertEqual(list(self.queryable1.distinct()), [])

    def test_distinct_all_distinct(self):
        self.assertEqual(list(self.queryable2.distinct()), [1, 2, 3, 4, 5])

    def test_distinct_some_distinct(self):
        self.assertEqual(list(self.queryable3.distinct()), [1, 2, 3, 4, 5, 6])

    def test_distinct_one_distinct(self):
        self.assertEqual(list(self.queryable4.distinct()), [1])

    def test_distinct_empty_with_key_selector(self):
        self.assertEqual(list(self.queryable1.distinct(lambda x: x % 2)), [])

    def test_distinct_all_distinct_with_key_selector(self):
        self.assertEqual(
            list(self.queryable2.distinct(lambda x: x % 2)), [1, 2])

    def test_distinct_some_distinct_with_key_selector(self):
        self.assertEqual(
            list(self.queryable3.distinct(lambda x: x % 2)), [1, 2])

    def test_distinct_one_distinct_with_key_selector(self):
        self.assertEqual(list(self.queryable4.distinct(lambda x: x % 2)), [1])

    def test_distinct_key_selector_type_error(self):
        self.assertRaises(TypeError, self.queryable2.distinct, 100)
