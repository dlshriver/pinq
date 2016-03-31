"""
pylinq: LINQ for Python
~~~~~~~~~~~~~~~~~~~~~~~

A LINQ implementation in Python for querying iterable datatypes.
Basic usage:

    >>> q = as_queryable(range(10)).where(lambda x: x % 2 == 0).to_list()
    [0, 2, 4, 6, 8]

pylinq supports querying any iterable data type.

:copyright: (c) 2016 by David Shriver.
:license: MIT, see LICENSE for more details.
"""

from .api import *
