"""
Tests for the pylinq api.
"""

import unittest
import pinq


class api_tests(unittest.TestCase):

    def test_as_queryable_iterable(self):
        self.assertEqual(list(pinq.as_queryable([1, 2, 3])), [1, 2, 3])

    def test_as_queryable_iterator(self):
        self.assertEqual(list(pinq.as_queryable(iter([1, 2, 3]))), [1, 2, 3])

    def test_as_queryable_type_error(self):
        self.assertRaises(TypeError, pinq.as_queryable, 100)
