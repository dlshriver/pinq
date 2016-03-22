"""
pylinq.queryable
~~~~~~~~~~~~~~~~

This module implements the Queryable class for querying iterables using the LINQ api.

:copyright: (c) 2016 by David Shriver.
:license: MIT, see LICENSE for more details.
"""

from collections import Iterable
from copy import copy
from functools import reduce
from itertools import tee, zip_longest
from .query import Query


class _Queryable(object):

    def __init__(self, iterable):
        self.iterable = iterable
        self._queries = []

    def _clone(self):
        clone = _Queryable(self.iterable)
        clone._queries = copy(self._queries)
        return clone

    def __iter__(self):
        self.iterable, iterable_copy = tee(self.iterable)
        iterator = iter(iterable_copy)
        for query in self._queries:
            iterator = Query.parse(iterator, query)
        for item in iterator:
            yield item

    # LINQ operations

    def aggregate(self, accumulator, seed=None, selector=None):
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
        if not callable(condition):
            raise TypeError("Value for argument 'condition' is not callable.")
        for item in self:
            if not condition(item):
                return False
        return True

    def any(self, condition=None):
        if condition is None:
            condition = lambda x: True
        elif not callable(condition):
            raise TypeError("Value for argument 'condition' is not callable.")
        for item in self:
            if condition(item):
                return True
        return False

    def average(self, transform=None):
        if transform is None:
            transform = lambda i: i
        elif not callable(transform):
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
        if not isinstance(to_type, type):
            raise TypeError("Value for argument 'to_type' is not a type.")
        return self._clone()._cast(to_type)

    def _concat(self, other):
        self._queries.append((Query.concat, other))
        return self

    def concat(self, other):
        if not isinstance(other, Iterable):
            raise TypeError("Value for argument 'iterable' is not iterable.")
        return self._clone()._concat(other)

    def contains(self, item, comparer=None):
        if comparer is None:
            comparer = lambda i1, i2: i1 == i2
        elif not callable(comparer):
            raise TypeError("Value for argument 'comparer' is not callable.")
        for i in self:
            if comparer(i, item):
                return True
        return False

    def count(self, condition=None):
        if condition is not None:
            return self._clone().where(condition).count()
        else:
            cnt = 0
            for _ in self:
                cnt += 1
            return cnt

    def default_if_empty(self):
        if self.empty():
            default = self._clone()
            default.iterable = [None]
            return default
        return self

    def _difference(self, iterable, key1=None, key2=None):
        self._queries.append((Query.difference, iterable, key1, key2))
        return self

    def difference(self, iterable, key1=None, key2=None):
        if not isinstance(iterable, Iterable):
            raise TypeError("Value for argument 'iterable' is not iterable.")
        if key1 is None:
            key1 = lambda x: x
        elif not callable(key1):
            raise TypeError("Value for argument 'key1' is not callable.")
        if key2 is None:
            key2 = key1
        elif not callable(key2):
            raise TypeError("Value for argument 'key2' is not callable.")
        return self._clone()._difference(iterable, key1, key2)

    def _distinct(self, key):
        self._queries.append((Query.distinct, key, {}))
        return self

    def distinct(self, key=None):
        if key is None:
            key = lambda x: x
        elif not callable(key):
            raise TypeError("Value for argument 'key' is not callable.")
        return self._clone()._distinct(key)

    def element_at(self, position):
        if not isinstance(position, int):
            raise TypeError("Value for argument 'position' is not an integer.")
        return list(self)[position]

    def element_at_or_default(self, position):
        try:
            return self.element_at(position)
        except IndexError:
            return None

    def empty(self):
        return len(list(self)) == 0

    def first(self, condition=None):
        if condition is None:
            condition = lambda x: True
        elif not callable(condition):
            raise TypeError("Value for argument 'condition' is not callable.")
        cnt = 0
        for item in self:
            cnt += 1
            if condition(item):
                return item
        if cnt == 0:
            raise ValueError("The source iterable is empty.")
        raise ValueError("No element satisfies argument 'condition'.")

    def first_or_default(self, condition=None):
        if condition is None:
            condition = lambda x: True
        elif not callable(condition):
            raise TypeError("Value for argument 'condition' is not callable.")
        for item in self:
            if condition(item):
                return item
        return None

    def _group_by(self, key):
        self._queries.append((Query.groupby, key))
        return self

    def group_by(self, key):
        if not callable(key):
            raise TypeError("Value for argument 'key' is not callable.")
        return self._clone()._group_by(key)

    def _group_join(self, iterable, key1, key2, join_func):
        self._queries.append(
            (Query.groupjoin, iterable, key1, key2, join_func))
        return self

    def group_join(self, iterable, key1, key2, join_func):
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

    def intersect(self, iterable, key1=None, key2=None):
        if not isinstance(iterable, Iterable):
            raise TypeError("Value for argument 'iterable' is not iterable.")
        if key1 is None:
            key1 = lambda x: x
        elif not callable(key1):
            raise TypeError("Value for argument 'key1' is not callable.")
        if key2 is None:
            key2 = key1
        elif not callable(key2):
            raise TypeError("Value for argument 'key2' is not callable.")
        return self._clone()._intersect(iterable, key1, key2)

    def _join(self, iterable, key1, key2, join_func):
        self._queries.append((Query.join, iterable, key1, key2, join_func))
        return self

    def join(self, iterable, key1, key2, join_func):
        if not isinstance(iterable, Iterable):
            raise TypeError("Value for argument 'iterable' is not iterable.")
        if not callable(key1):
            raise TypeError("Value for argument 'key1' is not callable.")
        if not callable(key2):
            raise TypeError("Value for argument 'key2' is not callable.")
        if not callable(join_func):
            raise TypeError("Value for argument 'join_func' is not callable.")
        return self._clone()._join(iterable, key1, key2, join_func)

    def last(self, condition=None):
        if condition is None:
            condition = lambda x: True
        elif not callable(condition):
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

    def last_or_default(self, condition=None):
        if condition is None:
            condition = lambda x: True
        elif not callable(condition):
            raise TypeError("Value for argument 'condition' is not callable.")
        last_item = None
        for item in self:
            if condition(item):
                last_item = item
        return last_item

    def long_count(self, condition=None):
        return self.count(condition)

    def max(self, transform=None):
        if transform is None:
            return max(self)
        elif not callable(transform):
            raise TypeError("Value for argument 'transform' is not callable.")
        return max(map(transform, self))

    def min(self, transform=None):
        if transform is None:
            return min(self)
        elif not callable(transform):
            raise TypeError("Value for argument 'transform' is not callable.")
        return min(map(transform, self))

    def of_type(self, of_type):
        if not isinstance(of_type, type):
            raise TypeError("Value for argument 'of_type' is not a type.")
        condition = lambda x: isinstance(x, of_type)
        return self.where(condition)

    def _order_by(self, key):
        self._queries.append((Query.orderby, key))
        return self

    def order_by(self, key):
        if not callable(key):
            raise TypeError("Value for argument 'key' is not callable.")
        return self._clone()._order_by(key)

    def _order_by_descending(self, key):
        self._queries.append((Query.orderbydesc, key))
        return self

    def order_by_descending(self, key):
        if not callable(key):
            raise TypeError("Value for argument 'key' is not callable.")
        return self._clone()._order_by_descending(key)

    def _reverse(self):
        self._queries.append((Query.reverse,))
        return self

    def reverse(self):
        return self._clone()._reverse()

    def _select(self, selector):
        self._queries.append((Query.select, selector))
        return self

    def select(self, selector):
        if not callable(selector):
            raise TypeError("Value for argument 'selector' is not callable.")
        return self._clone()._select(selector)

    def _select_many(self, selector):
        self._queries.append((Query.selectmany, selector))
        return self

    def select_many(self, selector):
        if not callable(selector):
            raise TypeError("Value for argument 'selector' is not callable.")
        return self._clone()._select_many(selector)

    def sequence_equal(self, iterable, comparer=None):
        if not isinstance(iterable, Iterable):
            raise TypeError("Value for argument 'iterable' is not iterable.")
        if comparer is None:
            comparer = lambda x, y: x == y
        elif not callable(comparer):
            raise TypeError("Value for argument 'comparer' is not callable.")
        for item1, item2 in zip_longest(self, iterable, fillvalue=None):
            if not comparer(item1, item2):
                return False
        return True

    def single(self, condition=None):
        if condition is None:
            condition = lambda x: True
        elif not callable(condition):
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

    def single_or_default(self, condition=None):
        if condition is None:
            condition = lambda x: True
        elif not callable(condition):
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
        if not isinstance(num, int):
            raise TypeError("Value for argument 'num' is not an integer.")
        return self._clone()._skip(num)

    def _skip_while(self, condition):
        self._queries.append((Query.skipwhile, condition))
        return self

    def skip_while(self, condition):
        if not callable(condition):
            raise TypeError("Value for argument 'condition' is not callable.")
        return self._clone()._skip_while(condition)

    def sum(self, transform=None):
        if transform is None:
            return sum(self)
        elif not callable(transform):
            raise TypeError("Value for argument 'transform' is not callable.")
        return sum(map(transform, self))

    def _take(self, num):
        self._queries.append((Query.take, num))
        return self

    def take(self, num):
        if not isinstance(num, int):
            raise TypeError("Value for argument 'num' is not an integer.")
        return self._clone()._take(num)

    def _take_while(self, condition):
        self._queries.append((Query.takewhile, condition))
        return self

    def take_while(self, condition):
        if not callable(condition):
            raise TypeError("Value for argument 'condition' is not callable.")
        return self._clone()._take_while(condition)

    def _then_by(self, key):
        old_orderby = self._queries[-1]
        self._queries[-1] = (Query.orderby, key)
        self._queries.append(old_orderby)
        return self

    def then_by(self, key):
        if not callable(key):
            raise TypeError("Value for argument 'key' is not callable.")
        if (len(self._queries) == 0 or
                (self._queries[-1][0] & (Query.orderby | Query.orderbydesc)) == 0):
            raise ValueError("Cannot call 'then_by' on unordered Queryable.")
        return self._clone()._then_by(key)

    def _then_by_descending(self, key):
        old_orderby = self._queries[-1]
        self._queries[-1] = (Query.orderbydesc, key)
        self._queries.append(old_orderby)
        return self

    def then_by_descending(self, key):
        if not callable(key):
            raise TypeError("Value for argument 'key' is not callable.")
        if (len(self._queries) == 0 or
                (self._queries[-1][0] & (Query.orderby | Query.orderbydesc)) == 0):
            raise ValueError("Cannot call 'then_by' on unordered Queryable.")
        return self._clone()._then_by_descending(key)

    def to_dictionary(self, key_selector, value_selector=None):
        if not callable(key_selector):
            raise TypeError(
                "Value for argument 'key_selector' is not callable.")
        if value_selector is None:
            value_selector = lambda x: x
        elif not callable(value_selector):
            raise TypeError(
                "Value for argument 'value_selector' is not callable.")
        return dict(zip(map(key_selector, self), map(value_selector, self)))

    def to_list(self):
        return list(self)

    def _union(self, iterable, key1, key2):
        self._queries.append((Query.union, iterable, key1, key2))
        return self

    def union(self, iterable, key1=None, key2=None):
        if not isinstance(iterable, Iterable):
            raise TypeError("Value for argument 'iterable' is not iterable.")
        if key1 is None:
            key1 = lambda x: x
        elif not callable(key1):
            raise TypeError("Value for argument 'key1' is not callable.")
        if key2 is None:
            key2 = key1
        elif not callable(key2):
            raise TypeError("Value for argument 'key2' is not callable.")
        return self._clone()._union(iterable, key1, key2)

    def _where(self, condition):
        self._queries.append((Query.where, condition))
        return self

    def where(self, condition):
        if not callable(condition):
            raise TypeError("Value for argument 'condition' is not callable.")
        return self._clone()._where(condition)
