import unittest
import pinq


class queryable_last_or_default_tests(unittest.TestCase):

    def setUp(self):
        self.queryable0 = pinq.as_queryable([])
        self.queryable1 = pinq.as_queryable(range(1))
        self.queryable2 = pinq.as_queryable(range(1, 11))

    def test_last_or_default_only_element(self):
        self.assertEqual(self.queryable1.last_or_default(), 0)

    def test_last_or_default_many_elements(self):
        self.assertEqual(self.queryable2.last_or_default(), 10)

    def test_last_or_default_only_element_with_condition(self):
        self.assertEqual(self.queryable1.last_or_default(lambda x: x < 5), 0)

    def test_last_or_default_many_elements_with_condition(self):
        self.assertEqual(self.queryable2.last_or_default(lambda x: x < 5), 4)

    def test_last_or_default_many_elements_with_condition_true_last(self):
        self.assertEqual(self.queryable2.last_or_default(lambda x: x > 5), 10)

    def test_last_or_default_only_element_with_default_value(self):
        self.assertEqual(self.queryable1.last_or_default(default_value=-1), 0)

    def test_last_or_default_many_elements_with_default_value(self):
        self.assertEqual(self.queryable2.last_or_default(default_value=-1), 10)

    def test_last_or_default_only_element_with_condition_with_default_value(self):
        self.assertEqual(self.queryable1.last_or_default(
            lambda x: x < 5, 10), 0)

    def test_last_or_default_many_elements_with_condition_same_last_with_default_value(self):
        self.assertEqual(self.queryable2.last_or_default(
            lambda x: x < 5, 19), 4)

    def test_last_or_default_many_elements_with_condition_change_last_with_default_value(self):
        self.assertEqual(self.queryable2.last_or_default(
            lambda x: x > 5, -1), 10)

    def test_last_or_default_empty(self):
        self.assertEqual(self.queryable0.last_or_default(), None)

    def test_last_or_default_no_satisfying(self):
        self.assertEqual(self.queryable2.last_or_default(
            lambda x: x > 100), None)

    def test_last_or_default_empty_with_default_value(self):
        self.assertEqual(self.queryable0.last_or_default(default_value=-1), -1)

    def test_last_or_default_no_satisfying_with_default_value(self):
        self.assertEqual(self.queryable2.last_or_default(
            lambda x: x > 100, -1), -1)

    def test_last_or_default_predicate_type_error(self):
        self.assertRaises(TypeError, self.queryable1.last_or_default, 100)
