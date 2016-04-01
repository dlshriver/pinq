import unittest
import pinq


class queryable_average_tests(unittest.TestCase):

    def setUp(self):
        self.queryable = pinq.as_queryable(range(1, 11))

    def test_average_no_transform(self):
        self.assertEqual(self.queryable.average(), 5.5)

    def test_average_with_transform(self):
        self.assertEqual(self.queryable.average(lambda x: x * 2), 11.0)

    def test_average_transform_type_error(self):
        self.assertRaises(TypeError, self.queryable.average, 100)
