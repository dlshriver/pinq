"""
Tests for the pylinq api.
"""

import unittest
import pinq


class api_tests(unittest.TestCase):

    def test_as_queryable(self):
        self.assertEqual(list(pinq.as_queryable([1, 2, 3])), [1, 2, 3])
        self.assertRaises(TypeError, pinq.as_queryable, 100)
