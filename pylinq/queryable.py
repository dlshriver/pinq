"""
pylinq.queryable
~~~~~~~~~~~~~~~~

This module implements the Queryable class for querying iterables using the LINQ api.

:copyright: (c) 2016 by David Shriver.
:license: MIT, see LICENSE for more details.
"""

from __future__ import division
from collections import Iterable, Iterator
from functools import reduce
from itertools import tee
try:
    from itertools import zip_longest
except ImportError:
    from itertools import izip_longest as zip_longest
from .query import Query


class Queryable(object):
    """A wrapper for iterable objects to allow querying of the underlying data.
    """

    def __init__(self, iterable):
        self.iterable = iterable
        self._queries = []

    def __repr__(self):
        return repr(self.iterable)

    def _clone(self):
        clone = Queryable(iter(self))
        return clone

    def __iter__(self):
        if isinstance(self.iterable, Iterator):
            self.iterable, iterable_copy = tee(self.iterable)
            iterator = iterable_copy
        else:
            iterator = iter(self.iterable)
        for query in self._queries:
            iterator = Query.parse(iterator, query)
        for item in iterator:
            yield item

    # LINQ operations

    def aggregate(self, accumulator, seed=None, selector=None):
        """Applies an accumulator function over a sequence.

        :param accumulator: accumulator function to apply to the underlying sequence.
        :type accumulator: function
        :param seed: (optional) initial accumulator value.
        :param selector: (optional) selector function to apply to final accumulator value.
        :type selector: function
        :return: accumulated value
        :raises TypeError: if accumulator is not callable
        :raises TypeError: if selector is not callable
        """
        if not callable(accumulator):
            raise TypeError(
                "Value for argument 'accumulator' is not callable.")
        if selector is not None and not callable(selector):
            raise TypeError("Value for argument 'selector' is not callable.")
        if selector is not None:
            return selector(reduce(accumulator, self, seed))
        if seed is not None:
            return reduce(accumulator, self, seed)
        return reduce(accumulator, self)

    def all(self, condition):
        """Determines whether all elements of the sequence satisfy a condition.

        :param condition: condition to check.
        :type condition: function
        :return: true if all values satisfy the condition, false otherwise
        :rtype: bool
        :raise TypeError: if condition is not callable
        """
        if not callable(condition):
            raise TypeError("Value for argument 'condition' is not callable.")
        for item in self:
            if not condition(item):
                return False
        return True

    def any(self, condition=lambda x: True):
        """Determines whether any element of the sequence satisfy a condition.

        :param condition: (optional) condition to check.
        :type condition: function
        :return: true if any value satisfies the condition, false otherwise
        :rtype: bool
        :raise TypeError: if condition is not callable
        """
        if not callable(condition):
            raise TypeError("Value for argument 'condition' is not callable.")
        for item in self:
            if condition(item):
                return True
        return False

    def average(self, transform=lambda i: i):
        """Computes the average of a sequence of numeric values.

        :param transform: (optional) transform function to invoke on each element of the sequence.
        :type transform: function
        :return: the average of the elements of the sequence
        :rtype: int or float
        :raise TypeError: if transform is not callable
        """
        if not callable(transform):
            raise TypeError("Value for argument 'transform' is not callable.")
        count = 0
        value_sum = 0
        for item in self:
            count += 1
            value_sum += transform(item)
        return value_sum / count

    def _cast(self, to_type):
        self._queries.append((Query.select, to_type))
        return self

    def cast(self, to_type):
        """Casts the elements of the sequence to the specified type.

        :param to_type: the type to cast elements to.
        :type to_type: type
        :return: the elements of the sequence cast to the specified type
        :rtype: :class:`Queryable <Queryable>` object
        :raise TypeError: if to_type is not a type
        """
        if not isinstance(to_type, type):
            raise TypeError("Value for argument 'to_type' is not a type.")
        return self._clone()._cast(to_type)

    def _concat(self, other):
        self._queries.append((Query.concat, other))
        return self

    def concat(self, other):
        """Concatenates two sequences.

        :param other: the sequence to concatenate.
        :type other: Iterable
        :return: a sequence containing the elements from this sequence and the sequence other
        :rtype: :class:`Queryable <Queryable>` object
        :raise TypeError: if other is not Iterable
        """
        if not isinstance(other, Iterable):
            raise TypeError("Value for argument 'iterable' is not iterable.")
        return self._clone()._concat(other)

    def contains(self, item, comparer=lambda i1, i2: i1 == i2):
        """Determines whether a sequence contains a specified element.

        :param item: the element being checked for.
        :param comparer: (optional) the comparer to check for equality.
        :type comparer: function
        :return: true if item is in the sequence, false otherwise
        :raise TypeError: if comparer is not callable
        """
        if not callable(comparer):
            raise TypeError("Value for argument 'comparer' is not callable.")
        for i in self:
            if comparer(i, item):
                return True
        return False

    def count(self, condition=lambda x: True):
        """Return the number of elements in a sequence.

        :param condition: (optional) condition for counting elements.
        :type condition: function
        :return: the number of elements in the sequence
        :rtype: int
        :raise TypeError: if condition is not callable
        """
        if not callable(condition):
            raise TypeError("Value for argument 'condition' is not callable.")
        cnt = 0
        for element in self:
            if condition(element):
                cnt += 1
        return cnt

    def default_if_empty(self, default_value=None):
        """Returns the elements of this sequence or the default value if the sequence is empty.

        :param default_value: (optional) the default value to return if the sequence is empty.
        :return: the elements of the sequence or the default value if the sequence is empty.
        :rtype: :class:`Queryable <Queryable>` object
        """
        if self.empty():
            default = self._clone()
            default.iterable = [default_value]
            return default
        return self

    def _difference(self, iterable, key1=None, key2=None):
        self._queries.append((Query.difference, iterable, key1, key2))
        return self

    def difference(self, iterable, key1=lambda x: x, key2=lambda x: x):
        """Produces the set difference of two sequences.

        :param iterable: the values to remove.
        :type iterable: Iterable
        :param key1: (optional) key selector for elements of this sequence
        :type key1: function
        :param key2: (optional) key selector for elements of iterable
        :type key2: function
        :return: the set difference of this sequence and iterable
        :rtype: :class:`Queryable <Queryable>` object
        :raise TypeError: if iterable is not iterable
        :raise TypeError: if key1 is not callable
        :raise TypeError: if key2 is not callable
        """
        if not isinstance(iterable, Iterable):
            raise TypeError("Value for argument 'iterable' is not iterable.")
        if not callable(key1):
            raise TypeError("Value for argument 'key1' is not callable.")
        if not callable(key2):
            raise TypeError("Value for argument 'key2' is not callable.")
        return self._clone()._difference(iterable, key1, key2)

    def _distinct(self, key):
        self._queries.append((Query.distinct, key, {}))
        return self

    def distinct(self, key=lambda x: x):
        """Returns distinct elements from the sequence.

        :param key: (optional) the key to use for comparisons.
        :type key: function
        :return: distinct elements of the sequence
        :rtype: :class:`Queryable <Queryable>` object
        :raise TypeError: if key is not callable
        """
        if not callable(key):
            raise TypeError("Value for argument 'key' is not callable.")
        return self._clone()._distinct(key)

    def element_at(self, position):
        """Returns the element at a specified position in the sequence.

        :param position: the position of the element to retreive
        :type position: int
        :return: the element at the specified position
        :raise TypeError: if position is not an int
        """
        if not isinstance(position, int):
            raise TypeError("Value for argument 'position' is not an integer.")
        return list(self)[position]

    def element_at_or_default(self, position):
        """Returns the element at the specified position or a default value if it is empty.

        :param position: the position of the element to retreive
        :type position: int
        :return: the element at the specified position
        :raise TypeError: if position is not an int
        """
        try:
            return self.element_at(position)
        except IndexError:
            return None

    def empty(self):
        """Returns true if the sequence is empty.

        :return: true if the sequence is empty, false otherwise
        :rtype: bool
        """
        return len(list(self)) == 0

    def except_values(self, iterable, key1=lambda x: x, key2=lambda x: x):
        """Produces the set difference of two sequences.

        :param iterable: the values to remove.
        :type iterable: Iterable
        :param key1: (optional) key selector for elements of this sequence
        :type key1: function
        :param key2: (optional) key selector for elements of iterable
        :type key2: function
        :return: the set difference of this sequence and iterable
        :rtype: :class:`Queryable <Queryable>` object
        :raise TypeError: if iterable is not iterable
        :raise TypeError: if key1 is not callable
        :raise TypeError: if key2 is not callable
        """
        return self.difference(iterable, key1, key2)

    def first(self, condition=lambda x: True):
        """Returns the first element in the sequence.

        :param condition: (optional) condition to apply to elements before selection.
        :type condition: function
        :return: the first element in the sequence that satisfies the condition.
        :raise TypeError: if condition is not callable
        :raise ValueError: if the sequence is empty
        :raise ValueError: if no element satisfies the condition
        """
        if not callable(condition):
            raise TypeError("Value for argument 'condition' is not callable.")
        cnt = 0
        for item in self:
            cnt += 1
            if condition(item):
                return item
        if cnt == 0:
            raise ValueError("The source iterable is empty.")
        raise ValueError("No element satisfies argument 'condition'.")

    def first_or_default(self, condition=lambda x: True):
        """Returns the first element in the sequence or a default value if empty.

        :param condition: (optional) condition to apply to elements before selection.
        :type condition: function
        :return: the first element in the sequence that satisfies the condition or a default value.
        :raise TypeError: if condition is not callable
        """
        if not callable(condition):
            raise TypeError("Value for argument 'condition' is not callable.")
        for item in self:
            if condition(item):
                return item
        return None

    def _group_by(self, key):
        self._queries.append((Query.groupby, key))
        return self

    def group_by(self, key):
        """Groups the elements of the sequence by the specified key.

        :param key: the key to group elements by.
        :type key: function
        :return: a queryable object of the groups and their key
        :rtype: :class:`Queryable <Queryable>` object
        :raise TypeError: if key is not callable
        """
        if not callable(key):
            raise TypeError("Value for argument 'key' is not callable.")
        return self._clone()._group_by(key)

    def _group_join(self, iterable, key1, key2, join_func):
        self._queries.append(
            (Query.groupjoin, iterable, key1, key2, join_func))
        return self

    def group_join(self, iterable, key1, key2, join_func):
        """Joins the elements of two sequences based on equality of keys and groups the results.

        :param iterable: the sequence to join with.
        :type iterable: Iterable
        :param key1: key selector for this sequence.
        :type key1: function
        :param key2: key selector for iterable.
        :type key2: function
        :param join_func: a function to join matched elements.
        :type join_func: function
        :return: a queryable of elements obtained by performing a grouped join on two sequences.
        :rtype: :class:`Queryable <Queryable>` object
        :raise TypeError: if iterable is not an Iterable
        :raise TypeError: if key1 is not callable
        :raise TypeError: if key2 is not callable
        :raise TypeError: if join_func is not callable
        """
        if not isinstance(iterable, Iterable):
            raise TypeError("Value for argument 'iterable' is not iterable.")
        if not callable(key1):
            raise TypeError("Value for argument 'key1' is not callable.")
        if not callable(key2):
            raise TypeError("Value for argument 'key2' is not callable.")
        if not callable(join_func):
            raise TypeError("Value for argument 'join_func' is not callable.")
        return self._clone()._group_join(iterable, key1, key2, join_func)

    def _intersect(self, iterable, key1, key2):
        self._queries.append((Query.intersect, iterable, key1, key2))
        return self

    def intersect(self, iterable, key1=lambda x: x, key2=lambda x: x):
        """Produces the set intersection of two sequences.

        :param iterable: an iterable to find an intersection with.
        :type iterable: Iterable
        :param key1: a key selector function for this sequence.
        :type key1: function
        :param key2: a key selector function for the provided sequence.
        :type key2: function
        :return: the intersection of two sequences
        :rtype: :class:`Queryable <Queryable>` object
        :raise TypeError: if iterable is not an Iterable
        :raise TypeError: if key1 is not callable
        :raise TypeError: if key2 is not callable
        """
        if not isinstance(iterable, Iterable):
            raise TypeError("Value for argument 'iterable' is not iterable.")
        if not callable(key1):
            raise TypeError("Value for argument 'key1' is not callable.")
        if not callable(key2):
            raise TypeError("Value for argument 'key2' is not callable.")
        return self._clone()._intersect(iterable, key1, key2)

    def _join(self, iterable, key1, key2, join_func):
        self._queries.append((Query.join, iterable, key1, key2, join_func))
        return self

    def join(self, iterable, key1, key2, join_func):
        """Joins the elements of two sequences based on matching keys.

        :param iterable: the iterable to join
        :type iterable: Iterable
        :param key1: a key selector function for this sequence
        :type key1: function
        :param key2: a key selector function for the provided sequence.
        :type key2: function
        :param join_func: a function to join matched elements.
        :type join_func: function
        :return: a queryable of elements obtained by joining two sequences.
        :rtype: :class:`Queryable <Queryable>` object
        :raise TypeError: if iterable is not an Iterable
        :raise TypeError: if key1 is not callable
        :raise TypeError: if key2 is not callable
        :raise TypeError: if join_func is not callable
        """
        if not isinstance(iterable, Iterable):
            raise TypeError("Value for argument 'iterable' is not iterable.")
        if not callable(key1):
            raise TypeError("Value for argument 'key1' is not callable.")
        if not callable(key2):
            raise TypeError("Value for argument 'key2' is not callable.")
        if not callable(join_func):
            raise TypeError("Value for argument 'join_func' is not callable.")
        return self._clone()._join(iterable, key1, key2, join_func)

    def last(self, condition=lambda x: True):
        """Returns the last element of a sequence.

        :param condition: (optional) the condition to apply to elements before selection.
        :type condition: function
        :return: the last element in the sequence satisfying the condition
        :raise TypeError: if condition is not callable
        :raise ValueError: if the source iterable is empty
        :raise ValueError: if no element satisfies condition
        """
        if not callable(condition):
            raise TypeError("Value for argument 'condition' is not callable.")
        last_item = None
        cnt = 0
        for item in self:
            cnt += 1
            if condition(item):
                last_item = item
        if last_item is not None:
            return last_item
        if cnt == 0:
            raise ValueError("The source iterable is empty.")
        raise ValueError("No element satisfies argument 'condition'.")

    def last_or_default(self, condition=lambda x: True):
        """Returns the last element of a sequence or a default if the sequence is empty.

        :param condition: (optional) the condition to apply to elements before selection.
        :type condition: function
        :return: the last element in the sequence satisfying the condition
        :raise TypeError: if condition is not callable
        """
        if not callable(condition):
            raise TypeError("Value for argument 'condition' is not callable.")
        last_item = None
        for item in self:
            if condition(item):
                last_item = item
        return last_item

    def long_count(self, condition=lambda x: True):
        """Return the number of elements in a sequence.

        :param condition: (optional) condition for counting elements.
        :type condition: function
        :return: the number of elements in the sequence
        :rtype: int
        :raise TypeError: if condition is not callable
        """
        return self.count(condition)

    def max(self, transform=lambda x: x):
        """Invokes a transform function on each element and returns the maximum value.

        :param transform: (optional) the transform function to apply to elements of the sequence.
        :type transform: function
        :return: the maximum value of the sequence
        :rtype: int
        :raise TypeError: if transform is not callable
        """
        if not callable(transform):
            raise TypeError("Value for argument 'transform' is not callable.")
        return max(map(transform, self))

    def min(self, transform=lambda x: x):
        """Invokes a transform function on each element and returns the minimum value.

        :param transform: (optional) the transform function to apply to elements of the sequence.
        :type transform: function
        :return: the minimum value of the sequence
        :rtype: int
        :raise TypeError: if transform is not callable
        """
        if not callable(transform):
            raise TypeError("Value for argument 'transform' is not callable.")
        return min(map(transform, self))

    def of_type(self, of_type):
        """Filters the elements of the sequence by the specified type.

        :param of_type: the type to keep.
        :type of_type: type
        :return: the elements of the sequence with the specified type
        :rtype: :class:`Queryable <Queryable>` object
        :raise TypeError: if of_type is not a type
        """
        if not isinstance(of_type, type):
            raise TypeError("Value for argument 'of_type' is not a type.")
        condition = lambda x: isinstance(x, of_type)
        return self.where(condition)

    def _order_by(self, key):
        self._queries.append((Query.orderby, key))
        return self

    def order_by(self, key):
        """Sorts the elements of the sequence in ascending order by the specified key.

        :param key: a function to extract a key from an element
        :type key: function
        :return: the elements of the sequence in ascending order based on key
        :rtype: :class:`Queryable <Queryable>` object
        :raise TypeError: if key is not callable
        """
        if not callable(key):
            raise TypeError("Value for argument 'key' is not callable.")
        return self._clone()._order_by(key)

    def _order_by_descending(self, key):
        self._queries.append((Query.orderbydesc, key))
        return self

    def order_by_descending(self, key):
        """Sorts the elements of the sequence in descending order by the specified key.

        :param key: a function to extract a key from an element
        :type key: function
        :return: the elements of the sequence in descending order based on key
        :rtype: :class:`Queryable <Queryable>` object
        :raise TypeError: if key is not callable
        """
        if not callable(key):
            raise TypeError("Value for argument 'key' is not callable.")
        return self._clone()._order_by_descending(key)

    def _reverse(self):
        self._queries.append((Query.reverse,))
        return self

    def reverse(self):
        """Reverses the order of elements in the sequence.

        :return: the sequence in reverse order
        :rtype: :class:`Queryable <Queryable>` object
        """
        return self._clone()._reverse()

    def _select(self, transform):
        self._queries.append((Query.select, transform))
        return self

    def select(self, transform):
        """Projects each element of the sequence into a new form.

        :param transform: the element transformation function
        :type transform: function
        :return: a sequence of transformed elements
        :rtype: :class:`Queryable <Queryable>` object
        :raise TypeError: if transform is not callable
        """
        if not callable(transform):
            raise TypeError("Value for argument 'transform' is not callable.")
        return self._clone()._select(transform)

    def _select_many(self, transform):
        self._queries.append((Query.selectmany, transform))
        return self

    def select_many(self, transform):
        """Projects elements of the sequence into an iterable and flattens the resulting sequence.

        :param transform: the element transformation function
        :type transform: function
        :return: a flattened sequence of transformed elements
        :rtype: :class:`Queryable <Queryable>` object
        :raise TypeError: if transform is not callable
        """
        if not callable(transform):
            raise TypeError("Value for argument 'transform' is not callable.")
        return self._clone()._select_many(transform)

    def sequence_equal(self, iterable, comparer=lambda x, y: x == y):
        """Determines whether two sequences are equal.

        :param iterable: the sequence to compare with.
        :type iterable: Iterable
        :param comparer: (optional) the comparison function to use.
        :type comparer: function
        :return: true if the sequences are equal, false otherwise
        :rtype: bool
        :raise TypeError: if iterable is not iterable
        :raise TypeError: if comparer is not callable
        """
        if not isinstance(iterable, Iterable):
            raise TypeError("Value for argument 'iterable' is not iterable.")
        if not callable(comparer):
            raise TypeError("Value for argument 'comparer' is not callable.")
        for item1, item2 in zip_longest(self, iterable, fillvalue=ValueError):
            if isinstance(item1, ValueError) or isinstance(item2, ValueError):
                return False
            if not comparer(item1, item2):
                return False
        return True

    def single(self, condition=lambda x: True):
        """Returns the only element of the sequence.

        :param condition: (optional) the condition to apply to elements.
        :type condition: function
        :return: the only element of the sequence that satisfies the condition
        :raise TypeError: if condition is not callable
        :raise ValueError: if more than one element satisfies condition
        :raise ValueError: if the sequence is empty
        :raise ValueError: if no element satisfies condition
        """
        if not callable(condition):
            raise TypeError("Value for argument 'condition' is not callable.")
        single_item = None
        cnt = 0
        for item in self:
            cnt += 1
            if condition(item):
                if single_item is not None:
                    raise ValueError(
                        "More than one element satisfies argument 'condition'")
                single_item = item
        if single_item is not None:
            return single_item
        if cnt == 0:
            raise ValueError("The source iterable is empty.")
        raise ValueError("No element satisfies argument 'condition'.")

    def single_or_default(self, condition=lambda x: True):
        """Returns the only element of the sequence or a default value if one does not exist.

        :param condition: (optional) the condition to apply to elements.
        :type condition: function
        :return: the only element of the sequence that satisfies the condition
        :raise TypeError: if condition is not callable
        :raise ValueError: if more than one element satisfies condition
        """
        if not callable(condition):
            raise TypeError("Value for argument 'condition' is not callable.")
        single_item = None
        for item in self:
            if condition(item):
                if single_item is not None:
                    raise ValueError(
                        "More than one element satisfies argument 'condition'")
                single_item = item
        return single_item

    def _skip(self, num):
        self._queries.append((Query.skip, num))
        return self

    def skip(self, num):
        """Skips a specified number of elements in the sequence and returns the remaining elements.

        :param num: the number of elements to skip
        :type num: int
        :return: a sequence containing the elements after position num
        :rtype: :class:`Queryable <Queryable>` object
        :raise TypeError: if num is not an int
        """
        if not isinstance(num, int):
            raise TypeError("Value for argument 'num' is not an integer.")
        return self._clone()._skip(num)

    def _skip_while(self, condition):
        self._queries.append((Query.skipwhile, condition))
        return self

    def skip_while(self, condition):
        """Skip elements of the sequence while the specified condition is true.

        :param condition: the condition to check for.
        :type condition: function
        :return: elements of the sequence starting at the first item to fail the specified condition
        :rtype: :class:`Queryable <Queryable>` object
        :raise TypeError: if condition is not callable
        """
        if not callable(condition):
            raise TypeError("Value for argument 'condition' is not callable.")
        return self._clone()._skip_while(condition)

    def sum(self, transform=lambda x: x):
        """Computes the sum of the sequence by invoking a transform on each element.

        :param transform: (optional) a transform function to apply to each element.
        :type transform: function
        :return: the sum of the elements of the sequence
        :rtype: int
        :raise TypeError: if transform is not callable
        """
        if not callable(transform):
            raise TypeError("Value for argument 'transform' is not callable.")
        return sum(map(transform, self))

    def _take(self, num):
        self._queries.append((Query.take, num))
        return self

    def take(self, num):
        """Returns a specified number of elements from the start of the sequence.

        :param num: the number of elements to take.
        :type num: int
        :return: the specified number of elements from the start of the sequence
        :rtype: :class:`Queryable <Queryable>` object
        :raise TypeError: if num is not an int
        """
        if not isinstance(num, int):
            raise TypeError("Value for argument 'num' is not an integer.")
        return self._clone()._take(num)

    def _take_while(self, condition):
        self._queries.append((Query.takewhile, condition))
        return self

    def take_while(self, condition):
        """Returns a elements from the start of the sequence while the specified condition holds.

        :param condition: the condition to check.
        :type condition: function
        :return: the elements from the start of the sequence that satisfy the condition
        :rtype: :class:`Queryable <Queryable>` object
        :raise TypeError: if condition is not callable
        """
        if not callable(condition):
            raise TypeError("Value for argument 'condition' is not callable.")
        return self._clone()._take_while(condition)

    def _then_by(self, old_orderby, key):
        self._queries.append((Query.orderby, key))
        self._queries.append(old_orderby)
        return self

    def then_by(self, key):
        """Performs a subsequenct ordering on the elements of an ordered sequence.

        :param key: a function to extract a key to use for comparisons
        :type key: function
        :return: the elements of the sequence in ascending order according to the key
        :rtype: :class:`Queryable <Queryable>` object
        :raise TypeError: if key is not callable
        :raise ValueError: if the sequence is not ordered
        """
        if not callable(key):
            raise TypeError("Value for argument 'key' is not callable.")
        if (len(self._queries) == 0 or
                (self._queries[-1][0] & (Query.orderby | Query.orderbydesc)) == 0):
            raise ValueError("Cannot call 'then_by' on unordered Queryable.")
        return self._clone()._then_by(self._queries[-1], key)

    def _then_by_descending(self, old_orderby, key):
        self._queries.append((Query.orderbydesc, key))
        self._queries.append(old_orderby)
        return self

    def then_by_descending(self, key):
        """Performs a subsequenct ordering on the elements of an ordered sequence.

        :param key: a function to extract a key to use for comparisons
        :type key: function
        :return: the elements of the sequence in descending order according to the key
        :rtype: :class:`Queryable <Queryable>` object
        :raise TypeError: if key is not callable
        :raise ValueError: if the sequence is not ordered
        """
        if not callable(key):
            raise TypeError("Value for argument 'key' is not callable.")
        if (len(self._queries) == 0 or
                (self._queries[-1][0] & (Query.orderby | Query.orderbydesc)) == 0):
            raise ValueError("Cannot call 'then_by' on unordered Queryable.")
        return self._clone()._then_by_descending(self._queries[-1], key)

    def to_dictionary(self, key_selector, value_selector=lambda x: x):
        """Creates a dictionary object according to the specified key selector function.

        :param key_selector: a function to extract the key for the dictionary entry
        :type key_selector: function
        :param value_selector: (optional) a function to extract the value for the dictionary entry
        :type value_selector: function
        :return: a dictionary of the elements in the sequence
        :rtype: dict
        :raise TypeError: if key_selector is not callable
        :raise TypeError: if value_selector is not callable
        """
        if not callable(key_selector):
            raise TypeError(
                "Value for argument 'key_selector' is not callable.")
        if not callable(value_selector):
            raise TypeError(
                "Value for argument 'value_selector' is not callable.")
        return dict(zip(map(key_selector, self), map(value_selector, self)))

    def to_list(self):
        """Creates a list object from the sequence.

        :return: a list of the elements in the sequence
        :rtype: list
        """
        return list(self)

    def _union(self, iterable, key1, key2):
        self._queries.append((Query.union, iterable, key1, key2))
        return self

    def union(self, iterable, key1=lambda x: x, key2=lambda x: x):
        """Returns the set union of two sequences.

        :param iterable: the second sequence for the union
        :type iterable: Iterable
        :param key1: (optional) a function to extract a key for elements of the first sequence.
        :type key1: function
        :param key2: (optional) a function to extract a key for elements of the second sequence.
        :type key2: function
        :return: the set union of the two sequences
        :rtype: :class:`Queryable <Queryable>` object
        :raise TypeError: if iterable is not an Iterable
        :raise TypeError: if key1 is not callable
        :raise TypeError: if key2 is not callable
        """
        if not isinstance(iterable, Iterable):
            raise TypeError("Value for argument 'iterable' is not iterable.")
        if not callable(key1):
            raise TypeError("Value for argument 'key1' is not callable.")
        if not callable(key2):
            raise TypeError("Value for argument 'key2' is not callable.")
        return self._clone()._union(iterable, key1, key2)

    def _where(self, condition):
        self._queries.append((Query.where, condition))
        return self

    def where(self, condition):
        """Filters the sequence of values based on the specified condition.

        :param condition: the condition an element must meet
        :type condition: function
        :return: the elements of the sequence for which the condition is True
        :rtype: :class:`Queryable <Queryable>` object
        :raise TypeError: if condition is not callable
        """
        if not callable(condition):
            raise TypeError("Value for argument 'condition' is not callable.")
        return self._clone()._where(condition)
