import unittest
import pinq


class queryable_order_by_descending_tests(unittest.TestCase):

    def setUp(self):
        self.queryable1 = pinq.as_queryable(range(1, 11))
        self.queryable2 = pinq.as_queryable(range(10, 0, -1))

    def test_order_by_descending(self):
        self.assertEqual(list(self.queryable2.order_by_descending(lambda x: x)), [
            10, 9, 8, 7, 6, 5, 4, 3, 2, 1])

    def test_order_by_descending_twice(self):
        self.assertEqual(list(self.queryable2.order_by_descending(lambda x: x).order_by_descending(
            lambda x: -x)), [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    def test_order_by_descending_in_order(self):
        self.assertEqual(list(self.queryable1.order_by_descending(lambda x: x)), [
            10, 9, 8, 7, 6, 5, 4, 3, 2, 1])

    def test_order_by_descending_key_selector_type_error(self):
        self.assertRaises(
            TypeError, self.queryable1.order_by_descending, "nothing")
