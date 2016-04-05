"""
pinq.tests
~~~~~~~~~~~~

Loads all tests for pinq and runs them.
"""

import unittest

unittest.TextTestRunner(verbosity=1).run(unittest.TestLoader().discover("./tests"))
