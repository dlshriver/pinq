"""
pylinq.api
~~~~~~~~~~

This module implements the pylinq api.

:copyright: (c) 2016 by David Shriver.
:license: MIT, see LICENSE for more details.
"""

from collections import Iterable
from .queryable import _Queryable

def as_queryable(iterable, cacheable=False):
    if not isinstance(iterable, Iterable):
        raise TypeError("Object must be iterable.")
    return _Queryable(iterable)
