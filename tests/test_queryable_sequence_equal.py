import unittest
import pinq


class queryable_sequence_equal_tests(unittest.TestCase):

    def setUp(self):
        self.queryable1 = pinq.as_queryable(range(1, 11))
        self.queryable2 = pinq.as_queryable(range(1, 11))
        self.queryable3 = pinq.as_queryable(range(1, 21, 2))
        self.queryable4 = pinq.as_queryable(range(1, 12))

    def test_sequence_equal_true(self):
        self.assertEqual(self.queryable1.sequence_equal(self.queryable1), True)
        self.assertEqual(self.queryable1.sequence_equal(self.queryable2), True)

    def test_sequence_equal_false_different_elements(self):
        self.assertEqual(self.queryable1.sequence_equal(
            self.queryable3), False)

    def test_sequence_equal_false_different_length(self):
        self.assertEqual(self.queryable1.sequence_equal(
            self.queryable4), False)

    def test_sequence_equal_true_with_comparer(self):
        self.assertEqual(self.queryable1.sequence_equal(
            self.queryable1, lambda x, y: x <= y), True)
        self.assertEqual(self.queryable1.sequence_equal(
            self.queryable2, lambda x, y: x <= y), True)

    def test_sequence_equal_false_with_comparer(self):
        self.assertEqual(self.queryable1.sequence_equal(
            self.queryable1, lambda x, y: x < y), False)

    def test_sequence_equal_other_type_error(self):
        self.assertRaises(TypeError, self.queryable1.sequence_equal, 103010455)

    def test_sequence_equal_equality_comparer_type_error(self):
        self.assertRaises(
            TypeError, self.queryable1.sequence_equal, self.queryable1, 103010455)
