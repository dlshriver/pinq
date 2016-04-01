import unittest
import pinq


class queryable_single_or_default_tests(unittest.TestCase):

    def setUp(self):
        self.queryable0 = pinq.as_queryable([])
        self.queryable1 = pinq.as_queryable(range(1, 11))
        self.queryable2 = pinq.as_queryable([2])

    def test_single_or_default_only_item(self):
        self.assertEqual(self.queryable2.single_or_default(), 2)

    def test_single_or_default_with_predicate(self):
        self.assertEqual(
            self.queryable1.single_or_default(lambda x: x > 9), 10)

    def test_single_or_default_multiple_values_value_error(self):
        self.assertRaises(ValueError, self.queryable1.single_or_default)

    def test_single_or_default_empty_sequence(self):
        self.assertEquals(self.queryable0.single_or_default(), None)

    def test_single_or_default_no_satisfying(self):
        self.assertEqual(self.queryable1.single_or_default(
            lambda x: x > 10), None)

    def test_single_or_default_empty_sequence(self):
        self.assertEquals(
            self.queryable0.single_or_default(default_value=-1), -1)

    def test_single_or_default_no_satisfying(self):
        self.assertEqual(self.queryable1.single_or_default(
            lambda x: x > 10, -1), -1)

    def test_single_or_default_multiple_values_with_predicate_value_error(self):
        self.assertRaises(
            ValueError, self.queryable1.single_or_default, lambda x: x > 5)

    def test_single_or_default_predicate_type_error(self):
        self.assertRaises(TypeError, self.queryable1.single_or_default, 10912)
