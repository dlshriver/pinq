import unittest
import pinq


class queryable_zip_tests(unittest.TestCase):

    def setUp(self):
        self.queryable1 = pinq.as_queryable(range(1, 11))
        self.queryable2 = pinq.as_queryable(["a", "b", "c"])

    def test_zip_diferent_lengths(self):
        self.assertEqual(list(self.queryable1.zip(self.queryable2, lambda x, y: (x, y))), [
            (1, "a"), (2, "b"), (3, "c")])

    def test_zip_same_length(self):
        self.assertEqual(list(self.queryable1.zip(
            self.queryable1, lambda x, y: x + y)), [2, 4, 6, 8, 10, 12, 14, 16, 18, 20])

    def test_zip_other_type_error(self):
        self.assertRaises(TypeError, self.queryable1.zip,
                          309415, lambda x, y: x + y)

    def test_zip_result_transform_type_error(self):
        self.assertRaises(TypeError, self.queryable1.zip, [309415], "wrong")
