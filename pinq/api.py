"""
pinq.api
~~~~~~~~

This module implements the pinq api.

:copyright: (c) 2016 by David Shriver.
:license: MIT, see LICENSE for more details.
"""

from collections import Iterable, Iterator
from .queryable import Queryable


def as_queryable(iterable):
    """Constructs a queryable object using `iterable` as the base data.

    :param iterable: iterable object to make queryable.
    :type iterable: Iterable
    :return: a queryable object with the specified iterable as the underlying data
    :rtype: :class:`Queryable <Queryable>` object
    :raise TypeError: if iterable is not an Iterable

    Usage::

      >>> import pinq
      >>> queryable = pinq.as_queryable(range(100))
    """
    if isinstance(iterable, Iterator):
        return Queryable(iterable)
    elif isinstance(iterable, Iterable):
        return Queryable(iter(iterable))
    raise TypeError("Object must be iterable.")
