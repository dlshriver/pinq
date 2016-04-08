"""
pinq.tests
~~~~~~~~~~~~

Loads all tests for pinq and runs them.
"""

from os import walk
import unittest

if __name__ == "__main__":
    tests = unittest.TestSuite()
    for _, _, filenames in walk("./tests"):
        for filename in filenames:
            if ".py" in filename and ".pyc" not in filename:
                tests.addTests(
                    unittest.TestLoader().loadTestsFromModule(__import__(filename[:-3])))
    unittest.TextTestRunner(verbosity=1).run(tests)
