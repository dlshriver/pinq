import unittest
import pinq


class queryable_difference_tests(unittest.TestCase):

    def setUp(self):
        self.queryable1 = pinq.as_queryable(range(1, 11))
        self.queryable2 = pinq.as_queryable(range(2, 10, 2))

    def test_difference_list(self):
        self.assertEqual(list(self.queryable1.difference(
            [1, 3, 5, 7, 9])), [2, 4, 6, 8, 10])

    def test_difference_list_remove_all(self):
        self.assertEqual(list(self.queryable1.difference(
            [1, 3, 5, 7, 9, 2, 4, 6, 8, 10])), [])

    def test_difference_list_remove_none(self):
        self.assertEqual(list(self.queryable1.difference(
            [15])), [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    def test_difference_queryable(self):
        self.assertEqual(list(self.queryable1.difference(
            self.queryable2)), [1, 3, 5, 7, 9, 10])

    def test_difference_queryable_more_removed_values(self):
        self.assertEqual(list(self.queryable2.difference(
            self.queryable1)), [])

    def test_difference_list_with_key_selector(self):
        self.assertEqual(list(self.queryable1.difference(
            [1, 3, 5, 7, 9], lambda x: x % 2)), [2, 4, 6, 8, 10])

    def test_difference_list_remove_all_with_key_selector(self):
        self.assertEqual(list(self.queryable1.difference(
            [1, 3, 5, 7, 9, 2, 4, 6, 8, 10], lambda x: x % 2)), [])

    def test_difference_list_remove_none_with_key_selector(self):
        self.assertEqual(list(self.queryable1.difference(
            [15], lambda x: x + 12)), [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    def test_difference_other_type_error(self):
        self.assertRaises(TypeError, self.queryable1.difference, 100)

    def test_difference_key_selector_type_error(self):
        self.assertRaises(
            TypeError, self.queryable1.difference, [1, 3, 6], 15)
