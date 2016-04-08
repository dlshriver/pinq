import unittest
import pinq


class queryable_element_at_or_default_tests(unittest.TestCase):

    def setUp(self):
        self.queryable = pinq.as_queryable(range(1, 11))

    def test_element_at_or_default_beginning(self):
        self.assertEqual(self.queryable.element_at_or_default(0), 1)

    def test_element_at_or_default_end(self):
        self.assertEqual(self.queryable.element_at_or_default(9), 10)

    def test_element_at_or_default_middle(self):
        self.assertEqual(self.queryable.element_at_or_default(5), 6)

    def test_element_at_or_default_index_type_error(self):
        self.assertRaises(
            TypeError, self.queryable.element_at_or_default, "apples")

    def test_element_at_or_default_index_negative(self):
        self.assertEqual(self.queryable.element_at_or_default(-3), None)

    def test_element_at_or_default_index_too_large(self):
        self.assertEqual(self.queryable.element_at_or_default(100129), None)

    def test_element_at_or_default_index_negative_with_default(self):
        self.assertEqual(self.queryable.element_at_or_default(-3, 10), 10)

    def test_element_at_or_default_index_too_large_with_default(self):
        self.assertEqual(self.queryable.element_at_or_default(100129, 10), 10)
