import unittest
import pinq


class queryable_sum_tests(unittest.TestCase):

    def setUp(self):
        self.queryable = pinq.as_queryable(range(1, 11))

    def test_sum(self):
        self.assertEqual(self.queryable.sum(), 55)

    def test_sum_with_transform(self):
        self.assertEqual(self.queryable.sum(lambda x: x % 2), 5)

    def test_sum_transform_type_error(self):
        self.assertRaises(TypeError, self.queryable.sum, 100)
