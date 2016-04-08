import unittest
import pinq


class queryable_take_while_tests(unittest.TestCase):

    def setUp(self):
        self.queryable = pinq.as_queryable(range(1, 11))

    def test_take_while(self):
        self.assertEqual(list(self.queryable.take_while(
            lambda x: x <= 5)), [1, 2, 3, 4, 5])

    def test_take_while_num_type_error(self):
        self.assertRaises(TypeError, self.queryable.take_while, "apple")
