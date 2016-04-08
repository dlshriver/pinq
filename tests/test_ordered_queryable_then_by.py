import unittest
import pinq


class ordered_queryable_then_by_tests(unittest.TestCase):

    def setUp(self):
        self.queryable1 = pinq.as_queryable(range(1, 11))
        self.queryable2 = pinq.as_queryable(range(10, 0, -1))

    def test_then_by(self):
        self.assertEqual(list(self.queryable2.order_by(lambda x: x % 2).then_by(lambda x: x)), [
            2, 4, 6, 8, 10, 1, 3, 5, 7, 9])

    def test_then_by_in_order(self):
        self.assertEqual(list(self.queryable1.order_by(lambda x: x).then_by(lambda x: x)), [
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    def test_then_by_key_selector_type_error(self):
        self.assertRaises(TypeError, self.queryable1.order_by(
            lambda x: x % 2).then_by, "nothing")
