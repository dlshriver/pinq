import unittest
import pinq


class queryable_cast_tests(unittest.TestCase):

    def setUp(self):
        self.queryable = pinq.as_queryable(range(1, 11))

    def test_cast_str(self):
        self.assertEqual(list(self.queryable.cast(str)), [
            "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])

    def test_cast_float(self):
        self.assertEqual(list(self.queryable.cast(float)), [
            1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0])

    def test_cast_to_type_type_error(self):
        self.assertRaises(TypeError, self.queryable.cast, 100)
