import unittest
import pinq


class queryable_first_tests(unittest.TestCase):

    def setUp(self):
        self.queryable0 = pinq.as_queryable([])
        self.queryable1 = pinq.as_queryable(range(1))
        self.queryable2 = pinq.as_queryable(range(1, 11))

    def test_first_only_element(self):
        self.assertEqual(self.queryable1.first(), 0)

    def test_first_many_elements(self):
        self.assertEqual(self.queryable2.first(), 1)

    def test_first_only_element_with_condition(self):
        self.assertEqual(self.queryable1.first(lambda x: x < 5), 0)

    def test_first_many_elements_with_condition_same_first(self):
        self.assertEqual(self.queryable2.first(lambda x: x < 5), 1)

    def test_first_many_elements_with_condition_change_first(self):
        self.assertEqual(self.queryable2.first(lambda x: x > 5), 6)

    def test_first_predicate_type_error(self):
        self.assertRaises(TypeError, self.queryable1.first, 100)

    def test_first_empty_value_error(self):
        self.assertRaises(ValueError, self.queryable0.first)

    def test_first_no_satisfying_value_error(self):
        self.assertRaises(ValueError, self.queryable2.first, lambda x: x > 100)
