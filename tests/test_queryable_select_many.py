import unittest
import pinq


class queryable_select_many_tests(unittest.TestCase):

    def setUp(self):
        self.queryable1 = pinq.as_queryable([[1, 2, 3], [2, 8, 10], [4, 5, 3]])
        self.queryable2 = pinq.as_queryable([{"a": [1, 3, 4], "list": [0, 9, 9]}, {
            "list": [5, 2, 4]}, {"Fun": "apple", "list": [1, 6, 7]}])
        self.queryable3 = pinq.as_queryable([[[1, 2, 3], [10, 11, 12]], [[9, 9, 4], [
            4, 5, 6], "a"], [[2, 8, 10], [7, 7, 7], [7, 8, 9]]])

    def test_select_many_identity(self):
        self.assertEqual(list(self.queryable1.select_many(lambda x: x)), [
            1, 2, 3, 2, 8, 10, 4, 5, 3])

    def test_select_many_attribute(self):
        self.assertEqual(list(self.queryable2.select_many(
            lambda x: x["list"])), [0, 9, 9, 5, 2, 4, 1, 6, 7])

    def test_select_many_with_index(self):
        self.assertEqual(list(self.queryable3.select_many(
            lambda x, i: x[i])), [1, 2, 3, 4, 5, 6, 7, 8, 9])

    def test_select_many_with_result_transform(self):
        self.assertEqual(list(self.queryable1.select_many(lambda x: x, lambda x, y: x + [y])), [
            [1, 2, 3, 1], [1, 2, 3, 2], [1, 2, 3, 3], [
                2, 8, 10, 2], [2, 8, 10, 8],
            [2, 8, 10, 10], [4, 5, 3, 4], [4, 5, 3, 5], [4, 5, 3, 3]])

    def test_select_many_selector_type_error(self):
        self.assertRaises(TypeError, self.queryable1.select_many, 100)

    def test_select_many_result_transform_type_error(self):
        self.assertRaises(
            TypeError, self.queryable1.select_many, lambda x: x, 100)
