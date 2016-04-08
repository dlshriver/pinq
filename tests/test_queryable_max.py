import unittest
import pinq


class queryable_max_tests(unittest.TestCase):

    def setUp(self):
        self.queryable1 = pinq.as_queryable(range(1, 11))
        self.queryable2 = pinq.as_queryable(range(10, 0, -1))
        self.queryable3 = pinq.as_queryable([1, 3, 4, 0, 9, 5])

    def test_max_first(self):
        self.assertEqual(self.queryable2.max(), 10)

    def test_max_last(self):
        self.assertEqual(self.queryable1.max(), 10)

    def test_max_middle(self):
        self.assertEqual(self.queryable3.max(), 9)

    def test_max_first_with_transform(self):
        self.assertEqual(self.queryable2.max(lambda x: x + 3), 13)

    def test_max_last_with_transform(self):
        self.assertEqual(self.queryable1.max(lambda x: x * 2), 20)

    def test_max_middle_with_transform(self):
        self.assertEqual(self.queryable3.max(lambda x: x % 4), 3)

    def test_max_transform_type_error(self):
        self.assertRaises(TypeError, self.queryable1.max, "square")
