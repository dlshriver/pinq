"""
Tests for the pylinq api.
"""

import sys
import unittest


class ItertoolsMock:

    def __getattr__(self, name):
        if name == "zip_longest":
            raise ImportError()
        if name == "izip_longest":
            return name
        if name == "__path__":
            return []
        return None


class FunctoolsMock:

    def __getattr__(self, name):
        if name == "lru_cache":
            raise ImportError()
        if name == "__path__":
            return []
        return None


class compat_tests(unittest.TestCase):

    def test_compat_lru_cache(self):
        sys.modules["functools"] = FunctoolsMock()
        if "pinq.compat" in sys.modules:
            del sys.modules["pinq.compat"]
        from pinq.compat import lru_cache
        self.assertEqual(lru_cache.__doc__,
                         "A default decorator if lru_cache does not exist.")
        function = lru_cache(1, False)(lambda x: x + 2)
        self.assertEqual(function(100), 102)

    def test_compat_zip_longest(self):
        sys.modules["itertools"] = ItertoolsMock()
        if "pinq.compat" in sys.modules:
            del sys.modules["pinq.compat"]
        from pinq.compat import zip_longest
        self.assertEqual(zip_longest, "izip_longest")
