import unittest
import pinq


class queryable_skip_while_tests(unittest.TestCase):

    def setUp(self):
        self.queryable = pinq.as_queryable(range(1, 11))

    def test_skip_while(self):
        self.assertEqual(list(self.queryable.skip_while(
            lambda x: x <= 5)), [6, 7, 8, 9, 10])

    def test_skip_while_predicate_type_error(self):
        self.assertRaises(TypeError, self.queryable.skip_while, "apple")
