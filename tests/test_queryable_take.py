import unittest
import pinq


class queryable_take_tests(unittest.TestCase):

    def setUp(self):
        self.queryable = pinq.as_queryable(range(1, 11))

    def test_take(self):
        self.assertEqual(list(self.queryable.take(5)), [1, 2, 3, 4, 5])

    def test_take_num_type_error(self):
        self.assertRaises(TypeError, self.queryable.take, "apple")
