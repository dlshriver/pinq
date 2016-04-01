import unittest
import pinq


class queryable_min_tests(unittest.TestCase):

    def setUp(self):
        self.queryable1 = pinq.as_queryable(range(1, 11))
        self.queryable2 = pinq.as_queryable(range(10, 0, -1))
        self.queryable3 = pinq.as_queryable([1, 3, 4, 0, 9, 5])

    def test_min_first(self):
        self.assertEqual(self.queryable1.min(), 1)

    def test_min_last(self):
        self.assertEqual(self.queryable2.min(), 1)

    def test_min_middle(self):
        self.assertEqual(self.queryable3.min(), 0)

    def test_min_first_with_transform(self):
        self.assertEqual(self.queryable1.min(lambda x: x + 3), 4)

    def test_min_last_with_transform(self):
        self.assertEqual(self.queryable2.min(lambda x: x * 2), 2)

    def test_min_middle_with_transform(self):
        self.assertEqual(self.queryable3.min(lambda x: x % 4), 0)

    def test_min_transform_type_error(self):
        self.assertRaises(TypeError, self.queryable1.min, "square")
