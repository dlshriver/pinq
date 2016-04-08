import unittest
import pinq


class queryable_intersect_tests(unittest.TestCase):

    def setUp(self):
        self.queryable1 = pinq.as_queryable(range(1, 11))
        self.queryable2 = pinq.as_queryable(range(3, 8, 2))
        self.queryable3 = pinq.as_queryable(range(100, 110))
        self.queryable4 = pinq.as_queryable(
            list(range(3, 8, 2)) + list(range(3, 8, 2)))

    def test_intersect_some(self):
        self.assertEqual(
            list(self.queryable1.intersect(self.queryable2)), [3, 5, 7])
        self.assertEqual(
            list(self.queryable2.intersect(self.queryable1)), [3, 5, 7])

    def test_intersect_all(self):
        self.assertEqual(
            list(self.queryable2.intersect(self.queryable2)), [3, 5, 7])

    def test_intersect_none(self):
        self.assertEqual(
            list(self.queryable1.intersect(self.queryable3)), [])

    def test_intersect_multiple_values(self):
        self.assertEqual(
            list(self.queryable1.intersect(self.queryable4)), [3, 5, 7])
        self.assertEqual(
            list(self.queryable4.intersect(self.queryable1)), [3, 5, 7])
        self.assertEqual(
            list(self.queryable4.intersect(self.queryable4)), [3, 5, 7])

    def test_intersect_some_with_key_selector(self):
        self.assertEqual(
            list(self.queryable1.intersect(self.queryable2, lambda x: x % 2)), [1])
        self.assertEqual(
            list(self.queryable2.intersect(self.queryable1, lambda x: x % 2)), [3])

    def test_intersect_all_with_key_selector(self):
        self.assertEqual(
            list(self.queryable2.intersect(self.queryable2, lambda x: x * 2)), [3, 5, 7])

    def test_intersect_none_with_key_selector(self):
        self.assertEqual(
            list(self.queryable1.intersect(self.queryable3, lambda x: x * 2)), [])

    def test_intersect_other_type_error(self):
        self.assertRaises(TypeError, self.queryable1.intersect, 1000)

    def test_intersect_key_selector_type_error(self):
        self.assertRaises(TypeError, self.queryable1.intersect, [1, 5], 100)
