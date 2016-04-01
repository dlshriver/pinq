import unittest
import pinq


class queryable_concat_tests(unittest.TestCase):

    def setUp(self):
        self.queryable1 = pinq.as_queryable(range(1, 11))
        self.queryable2 = pinq.as_queryable(range(11, 21))

    def test_concat_list(self):
        self.assertEqual(list(self.queryable1.concat(
            [11, 12, 13])), list(range(1, 14)))

    def test_concat_queryable(self):
        self.assertEqual(list(self.queryable1.concat(
            self.queryable2)), list(range(1, 21)))

    def test_concat_other_type_error(self):
        self.assertRaises(TypeError, self.queryable1.concat, 100)
