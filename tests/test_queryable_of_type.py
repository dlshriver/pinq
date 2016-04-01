import unittest
import pinq


class queryable_of_type_tests(unittest.TestCase):

    def setUp(self):
        self.queryable = pinq.as_queryable(
            [1, 2, 3.0, "apple", "banana", [2.1, 16], 0])

    def test_of_type_str(self):
        self.assertEqual(list(self.queryable.of_type(str)),
                         ["apple", "banana"])

    def test_of_type_float(self):
        self.assertEqual(list(self.queryable.of_type(float)), [3.0])

    def test_of_type_int(self):
        self.assertEqual(list(self.queryable.of_type(int)), [1, 2, 0])

    def test_of_type_list(self):
        self.assertEqual(list(self.queryable.of_type(list)), [[2.1, 16]])

    def test_of_type_of_type_type_error(self):
        self.assertRaises(TypeError, self.queryable.of_type, 100)
