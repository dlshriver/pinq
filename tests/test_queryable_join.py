import unittest
import pinq


class queryable_join_tests(unittest.TestCase):

    def setUp(self):
        self.queryable1 = pinq.as_queryable(range(1, 11))
        self.queryable2 = pinq.as_queryable(range(11, 21))

    def test_join_all(self):
        self.assertEqual(list(self.queryable1.join(
            self.queryable2, lambda x: x, lambda x: x - 10, lambda x: x)), [
                (1, 11), (2, 12), (3, 13), (4, 14), (5, 15), (6, 16), (7, 17),
                (8, 18), (9, 19), (10, 20)])

    def test_join_some(self):
        self.assertEqual(list(self.queryable1.join(
            self.queryable1, lambda x: x, lambda x: x % 3, lambda x: x)), [
                (1, 1), (1, 4), (1, 7), (1, 10), (2, 2), (2, 5), (2, 8)])

    def test_join_none(self):
        self.assertEqual(list(self.queryable1.join(
            self.queryable2, lambda x: x, lambda x: x, lambda x: x)), [])

    def test_join_some_transform_result(self):
        self.assertEqual(list(self.queryable1.join(
            self.queryable1, lambda x: x, lambda x: x % 3, lambda x, y: y)), [
                1, 4, 7, 10, 2, 5, 8])

    def test_join_other_type_error(self):
        self.assertRaises(TypeError, self.queryable1.join, 100,
                          lambda x: x, lambda x: x, lambda x: x)

    def test_join_key_selector_type_error(self):
        self.assertRaises(TypeError, self.queryable1.join, self.queryable1,
                          "ten", lambda x: x, lambda x: x)

    def test_join_other_key_selector_type_error(self):
        self.assertRaises(TypeError, self.queryable1.join, self.queryable1,
                          lambda x: x, "identity", lambda x: x)

    def test_join_result_transform_type_error(self):
        self.assertRaises(TypeError, self.queryable1.join, self.queryable1,
                          lambda x: x, lambda x: x, "test")
