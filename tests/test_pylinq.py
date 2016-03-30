"""
Tests for the pylinq api.
"""

import unittest
import pylinq


class pylinq_tests(unittest.TestCase):

    def test_as_queryable(self):
        self.assertEqual(list(pylinq.as_queryable([1, 2, 3])), [1, 2, 3])
        self.assertRaises(TypeError, pylinq.as_queryable, 100)
