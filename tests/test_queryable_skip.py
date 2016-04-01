import unittest
import pinq


class queryable_skip_tests(unittest.TestCase):

    def setUp(self):
        self.queryable = pinq.as_queryable(range(1, 11))

    def test_skip(self):
        self.assertEqual(list(self.queryable.skip(5)), [6, 7, 8, 9, 10])

    def test_skip_num_type_error(self):
        self.assertRaises(TypeError, self.queryable.skip, "apple")
