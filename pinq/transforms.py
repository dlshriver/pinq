"""
pinq.selectors
~~~~~~~~~~~~~~

This module implements common selector and transform functions.

:copyright: (c) 2016 by David Shriver.
:license: MIT, see LICENSE for more details.
"""


def identity(value):
    """Returns the identity function applied to the provided value.

    :param value: The value that will be returned.
    :return: The provided value.
    """
    return value


def select_i(index):
    """Returns a function that selects the argument with the specified index.

    :param index: The index of the argument to select.
    :type index: int
    :return: Returns a function that takes any number of arguments and selects
        the argument with the specified argument.
    """
    return lambda *args: args[index]
