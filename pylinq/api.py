"""
pylinq.api
~~~~~~~~~~

This module implements the pylinq api.

:copyright: (c) 2016 by David Shriver.
:license: MIT, see LICENSE for more details.
"""

from collections import Iterable
from .queryable import Queryable


def as_queryable(iterable):
    """Constructs a queryable object using `iterable` as the base data.

    :param iterable: iterable object to make queryable.
    :type iterable: Iterable
    :return: a queryable object with the specified iterable as the underlying data
    :rtype: :class:`Queryable <Queryable>` object
    :raise TypeError: if iterable is not an Iterable

    Usage::

      >>> import pylinq
      >>> queryable = pylinq.as_queryable(range(100))
      range(0, 100)
    """
    if not isinstance(iterable, Iterable):
        raise TypeError("Object must be iterable.")
    return Queryable(iterable)
