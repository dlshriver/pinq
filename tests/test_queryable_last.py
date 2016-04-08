import unittest
import pinq


class queryable_last_tests(unittest.TestCase):

    def setUp(self):
        self.queryable0 = pinq.as_queryable([])
        self.queryable1 = pinq.as_queryable(range(1))
        self.queryable2 = pinq.as_queryable(range(1, 11))

    def test_last_only_element(self):
        self.assertEqual(self.queryable1.last(), 0)

    def test_last_many_elements(self):
        self.assertEqual(self.queryable2.last(), 10)

    def test_last_only_element_with_condition(self):
        self.assertEqual(self.queryable1.last(lambda x: x < 5), 0)

    def test_last_many_elements_with_condition(self):
        self.assertEqual(self.queryable2.last(lambda x: x < 5), 4)

    def test_last_many_elements_with_condition_true_last(self):
        self.assertEqual(self.queryable2.last(lambda x: x > 5), 10)

    def test_last_predicate_type_error(self):
        self.assertRaises(TypeError, self.queryable1.last, 100)

    def test_last_empty_value_error(self):
        self.assertRaises(ValueError, self.queryable0.last)

    def test_last_no_satisfying_value_error(self):
        self.assertRaises(ValueError, self.queryable2.last, lambda x: x > 100)
