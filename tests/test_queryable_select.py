import unittest
import pinq


class queryable_select_tests(unittest.TestCase):

    def setUp(self):
        self.queryable = pinq.as_queryable(range(1, 11))

    def test_select_one_argument_selector(self):
        self.assertEqual(list(self.queryable.select(lambda x: x % 2)), [
            1, 0, 1, 0, 1, 0, 1, 0, 1, 0])

    def test_select_two_argument_selector(self):
        self.assertEqual(list(self.queryable.select(
            lambda x, y: x % (y // 2 + 1))), [0, 0, 1, 0, 2, 0, 3, 0, 4, 0])

    def test_select_selector_type_error(self):
        self.assertRaises(TypeError, self.queryable.select, 100)
