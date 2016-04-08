import unittest
import pinq


class queryable_single_tests(unittest.TestCase):

    def setUp(self):
        self.queryable0 = pinq.as_queryable([])
        self.queryable1 = pinq.as_queryable(range(1, 11))
        self.queryable2 = pinq.as_queryable([2])

    def test_single_only_item(self):
        self.assertEqual(self.queryable2.single(), 2)

    def test_single_with_predicate(self):
        self.assertEqual(self.queryable1.single(lambda x: x > 9), 10)

    def test_single_multiple_values_value_error(self):
        self.assertRaises(ValueError, self.queryable1.single)

    def test_single_multiple_values_with_predicate_value_error(self):
        self.assertRaises(ValueError, self.queryable1.single, lambda x: x > 5)

    def test_single_empty_sequence_value_error(self):
        self.assertRaises(ValueError, self.queryable0.single)

    def test_single_no_satisfying_value_error(self):
        self.assertRaises(ValueError, self.queryable1.single, lambda x: x > 10)

    def test_single_predicate_type_error(self):
        self.assertRaises(TypeError, self.queryable1.single, 10912)
