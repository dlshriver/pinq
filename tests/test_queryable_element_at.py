import unittest
import pinq


class queryable_element_at_tests(unittest.TestCase):

    def setUp(self):
        self.queryable = pinq.as_queryable(range(1, 11))

    def test_element_at_beginning(self):
        self.assertEqual(self.queryable.element_at(0), 1)

    def test_element_at_end(self):
        self.assertEqual(self.queryable.element_at(9), 10)

    def test_element_at_middle(self):
        self.assertEqual(self.queryable.element_at(5), 6)

    def test_element_at_index_type_error(self):
        self.assertRaises(TypeError, self.queryable.element_at, "apples")

    def test_element_at_index_error_negative(self):
        self.assertRaises(IndexError, self.queryable.element_at, -3)

    def test_element_at_index_error_too_large(self):
        self.assertRaises(IndexError, self.queryable.element_at, 100129)
