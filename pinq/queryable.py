"""
pinq.queryable
~~~~~~~~~~~~~~

This module implements the Queryable class for querying iterables using the LINQ api.

:copyright: (c) 2016 by David Shriver.
:license: MIT, see LICENSE for more details.
"""

from __future__ import division
from .compat import *
from .predicates import true
from .transforms import identity, select_i


class Queryable(object):
    """A wrapper for iterable objects to allow querying of the underlying data.
    """

    def __init__(self, iterator):
        self.iterator = iterator

    def __iter__(self):
        self.iterator, iterator = tee(self.iterator)
        for element in iterator:
            yield element

    def aggregate(self, accumulator, seed=None, result_transform=identity):
        """Applies an accumulator function over a sequence.

        :param accumulator: The accumulator function to apply.
        :type accumulator: function
        :param seed: (optional) The initial accumulator value.
        :param result_transform: (optional) A transform function to apply to the result.
        :type result_transform: function
        :return: The accumulated value.
        :raise TypeError: if 'accumulator' is not callable
        :raise TypeError: if 'result_transform' is not callable
        """
        if not callable(accumulator):
            raise TypeError(
                "Value for 'accumulator' is not callable.")
        if not callable(result_transform):
            raise TypeError(
                "Value for 'result_transform' is not callable.")
        if seed is not None:
            return result_transform(reduce(accumulator, self, seed))
        return result_transform(reduce(accumulator, self))

    def all(self, predicate):
        """Determines whether all elements of the sequence satisfy a condition.

        :param predicate: A function to test each element for a condition.
        :type predicate: function
        :return: True if every element satisfies the condition, or the sequence is empty.
        :rtype: bool
        :raise TypeError: if 'predicate' is not callable
        """
        if not callable(predicate):
            raise TypeError("Value for 'predicate' is not callable.")
        for element in self:
            if not predicate(element):
                return False
        return True

    def any(self, predicate=true):
        """Determines whether any element of the sequence satisfies a condition.

        :param predicate: (optional) A function to test each element for a condition.
        :type predicate: function
        :return: True if any element satisfies the condition.
        :rtype: bool
        :raise TypeError: if 'predicate' is not callable
        """
        if not callable(predicate):
            raise TypeError("Value for 'predicate' is not callable.")
        for element in self:
            if predicate(element):
                return True
        return False

    def average(self, transform=identity):
        """Computes the average of the elements in the sequence.

        :param transform: (optional) A transform function to invoke on each element of the sequence.
        :type transform: function:
        :return: The average value of the elements in the sequence.
        :rtype: float
        :raise TypeError: if 'transform' is not callable
        """
        if not callable(transform):
            raise TypeError("Value for 'transform' is not callable.")
        count = 0
        value_sum = 0
        for element in self:
            count += 1
            value_sum += transform(element)
        return value_sum / count

    def cast(self, to_type):
        """Casts the elements of the sequence to the specified type.

        :param to_type: The type to cast elements to.
        :type to_type: type
        :return: The elements of the sequence cast to the specified type.
        :rtype: :class:`Queryable`
        :raise TypeError: if 'to_type' is not callable
        """
        if not isinstance(to_type, type):
            raise TypeError("Value for 'to_type' is not a type.")
        return Queryable((to_type(element) for element in self))

    def concat(self, other):
        """Concatenates two sequences.

        :param other: The sequence to concatenate to this sequence.
        :type other: Iterable
        :return: A Queryable containing the concatenated elements of the two input sequences.
        :rtype: :class:`Queryable`
        :raise TypeError: if 'other' is not Iterable
        """
        if not isinstance(other, Iterable):
            raise TypeError("Value for 'other' is not an Iterable.")
        return Queryable(chain(self, other))

    def contains(self, value, equality_comparer=eq):
        """Determines whether the sequence contains the specified value.

        :param value: The value to find in the sequence.
        :param equality_comparer: (optional) An equality comparer to compare values.
        :type equality_comparer: function
        :return: True if the sequence contains the specified value.
        :rtype: bool
        :raise TypeError: if 'equality_comparer' is not callable
        """
        if not callable(equality_comparer):
            raise TypeError("Value for 'equality_comparer' is not callable.")
        for element in self:
            if equality_comparer(value, element):
                return True
        return False

    def count(self, predicate=true):
        """Returns the number of elements in the sequence.

        :param predicate: (optional) A function to test each element for a condition:
        :type predicate: function
        :return: The number of elements that satisfy the specified condition.
        :rtype: int
        :raise TypeError: if 'predicate' is not callable
        """
        if not callable(predicate):
            raise TypeError("Value for 'predicate' is not callable.")
        count = 0
        for element in self:
            if predicate(element):
                count += 1
        return count

    def default_if_empty(self, default_value=None):
        """Returns the sequence or a sequence with a single default value if the sequence is empty.

        :param default_value: (optional) The default value to return.
        :return:This sequence, or a sequence containing 'default_value' if it is empty.
        :rtype: :class:`Queryable`
        """
        for _ in self:
            return self
        return Queryable([default_value])

    def difference(self, other, key_selector=identity):
        """Returns the set difference of the two sequences.

        :param other: An iterable of elements to be removed from this sequence.
        :type other: Iterable
        :param key_selector: (optional) An function to select a key for comparing values.
        :type key_selector: function
        :return: The set difference of this sequence and the provided sequence.
        :rtype: :class:`Queryable`
        :raise TypeError: if 'other' is not an Interable
        :raise TypeError: if 'key_selector' is not callable
        """
        return self.except_values(other, key_selector)

    def distinct(self, key_selector=identity):
        """Returns distinct elements fromt the sequence.

        :param key_selector: (optional) An function to select a key for comparing values.
        :type key_selector: function
        :return: A sequence of distinct elements from this sequence.
        :rtype: :class:`Queryable`
        :raise TypeError: if 'key_selector' is not callable
        """
        if not callable(key_selector):
            raise TypeError("Value for 'key_selector' is not callable.")
        seen = {}

        def _distinct(value):
            key = key_selector(value)
            if key in seen:
                return False
            seen[key] = 1
            return True
        return Queryable((element for element in self if _distinct(element)))

    def element_at(self, index):
        """Returns the element at the specified location in the sequence.

        :param index: The zero-based index of the element to retrieve.
        :type index: int
        :return: The element at the specified location in the sequence.
        :raise TypeError: if 'index' is not an int
        :raise IndexError: if 'index' is less than zero or larger than the number of elements
        """
        if not isinstance(index, int):
            raise TypeError("Value for 'index' is not an integer.")
        elif index < 0:
            raise IndexError("The provided index is out of range.")
        count = 0
        for element in self:
            if count == index:
                return element
            count += 1
        raise IndexError("The provided index is out of range.")

    def element_at_or_default(self, index, default_value=None):
        """Returns the element at the specified index or a default value if it is out of range.

        :param index: The zero-based index of the element to retrieve.
        :type index: int
        :param default_value: (optional) The default value if the index is out of range.
        :return: The element at the specified location in the sequence.
        :raise TypeError: if 'index' is not an int
        """
        try:
            return self.element_at(index)
        except IndexError:
            return default_value

    def except_values(self, other, key_selector=identity):
        """Returns the set difference of the two sequences.

        :param other: An iterable of elements to be removed from this sequence.
        :type other: Iterable
        :param key_selector: (optional) An function to select a key for comparing values.
        :type key_selector: function
        :return: The set difference of this sequence and the provided sequence.
        :rtype: :class:`Queryable`
        :raise TypeError: if 'other' is not an Interable
        :raise TypeError: if 'key_selector' is not callable
        """
        if not isinstance(other, Iterable):
            raise TypeError("Value for 'other' is not an Iterable.")
        if not callable(key_selector):
            raise TypeError("Value for 'key_selector' is not callable.")

        @lru_cache(1, False)
        def _seen():
            return dict([(key_selector(element), 1) for element in other])

        def _removed(value):
            seen = _seen()
            key = key_selector(value)
            if key in seen:
                return True
            return False
        return Queryable((element for element in self if not _removed(element)))

    def first(self, predicate=true):
        """Returns the first element in the sequence.

        :param predicate: (optional) A function to test each element for a condition.
        :type predicate: function
        :return: The first element of the sequence satisfying the condition.
        :raise TypeError: if 'predicate' is not callable
        :raise ValueError: if the sequence is empty
        :raise ValueError: if no element satisfies the condition
        """
        if not callable(predicate):
            raise TypeError("Value for 'predicate' is not callable.")
        count = 0
        for element in self:
            count += 1
            if predicate(element):
                return element
        if count == 0:
            raise ValueError("The source sequence is empty.")
        raise ValueError("No element satisfies the predicate.")

    def first_or_default(self, predicate=true, default_value=None):
        """Returns the first element in the sequence or a default value if empty.

        :param predicate: (optional) A function to test each element for a condition.
        :type predicate: function
        :param default_value: (optional) The default value to return if empty.
        :return: The first element of the sequence satisfying the condition.
        :raise TypeError: if 'predicate' is not callable
        """
        if not callable(predicate):
            raise TypeError("Value for 'predicate' is not callable.")
        count = 0
        for element in self:
            count += 1
            if predicate(element):
                return element
        return default_value

    def group_by(self, key_selector, value_transform=identity, result_transform=identity):
        """Groups the elements of the sequence according to the specified key selector function.

        :param key_selector: A function to extract the key for each element.
        :type key_selector: function
        :param value_transform: A transform function to be applied to each element.
        :type value_transform: function
        :param result_transform: A transform function to be applied to each group.
        :type result_transform: function
        :return: A sequence where each element represents the transformation of a group and its key.
        :rtype: :class:`Queryable`
        :raise TypeError: if 'key_selector' is not callable
        :raise TypeError: if 'value_transform' is not callable
        :raise TypeError: if 'result_transform' is not callable
        """
        if not callable(key_selector):
            raise TypeError("Value for 'key_selector' is not callable.")
        if not callable(value_transform):
            raise TypeError("Value for 'value_transform' is not callable.")
        if not callable(result_transform):
            raise TypeError("Value for 'result_transform' is not callable.")
        if result_transform.__code__.co_argcount == 1:
            return Queryable((result_transform(
                (key, [value_transform(element) for element in group])) for key, group in groupby(
                    sorted(self, key=key_selector), key=key_selector)))
        else:
            return Queryable(
                (result_transform(key, [value_transform(element) for element in group])
                 for key, group in groupby(sorted(self, key=key_selector), key=key_selector)))

    def group_join(self, other, key_selector, other_key_selector, result_transform):
        """Correlates the elements of the two sequences and groups the results.

        :param other: The sequence to join this sequence.
        :type other: Iterable
        :param key_selector: A function to extract a key from each element of this sequence.
        :type key_selector: function
        :param other_key_selector: A function to extract a key from each element of 'other'.
        :type other_key_selector: function
        :param result_transform: A function to create a result from an item and its matching group.
        :type result_transform: function
        :return: The elements of the two sequences after performing a grouped join.
        :rtype: :class:`Queryable`
        :raise TypeError: if 'other' is not an Iterable
        :raise TypeError: if 'key_selector' is not callable
        :raise TypeError: if 'other_key_selector' is not callable
        :raise TypeError: if 'result_transform' is not callable
        """
        if not isinstance(other, Iterable):
            raise TypeError("Value for 'other' is not an Iterable.")
        if not callable(key_selector):
            raise TypeError("Value for 'key_selector' is not callable.")
        if not callable(other_key_selector):
            raise TypeError("Value for 'other_key_selector' is not callable.")
        if not callable(result_transform):
            raise TypeError("Value for 'result_transform' is not callable.")

        @lru_cache(1, False)
        def _other_groups():
            groups = defaultdict(list)
            for element in other:
                key = other_key_selector(element)
                groups[key].append(element)
            return groups
        if result_transform.__code__.co_argcount == 1:
            return Queryable((result_transform((
                element, _other_groups()[key_selector(element)])) for element in self))
        else:
            return Queryable((result_transform(
                element, _other_groups()[key_selector(element)]) for element in self))

    def intersect(self, other, key_selector=identity):
        """Returns the set intersection of the two sequences.

        :param other: A sequence to compute the intersection with.
        :type other: Iterable
        :param key_selector: (optional) A function to extract a key for each element for comparison.
        :type key_selector: function
        :return: A sequence of distinct elements that are in both of the provided seequences.
        :rtype: :class:`Queryable`
        :raise TypeError: if 'other' is not an Iterable
        :raise TypeError: if 'key_selector' is not callable
        """
        if not isinstance(other, Iterable):
            raise TypeError("Value for 'other' is not an Iterable.")
        if not callable(key_selector):
            raise TypeError("Value for 'key_selector' is not callable.")

        @lru_cache(1, False)
        def _other_set():
            return dict([(key_selector(element), 1) for element in other])

        seen = {}

        def _intersects(element):
            key = key_selector(element)
            if key in _other_set() and not key in seen:
                seen[key] = 1
                return True
            return False
        return Queryable((element for element in self if _intersects(element)))

    def join(self, other, key_selector, other_key_selector, result_transform):
        """Correlates the elements of the two sequences.

        :param other: The sequence to join this sequence.
        :type other: Iterable
        :param key_selector: A function to extract a key from each element of this sequence.
        :type key_selector: function
        :param other_key_selector: A function to extract a key from each element of 'other'.
        :type other_key_selector: function
        :param result_transform: A function to create a result from an item and its match.
        :type result_transform: function
        :return: The elements of the two sequences after performing an inner join.
        :rtype: :class:`Queryable`
        :raise TypeError: if 'other' is not an Iterable
        :raise TypeError: if 'key_selector' is not callable
        :raise TypeError: if 'other_key_selector' is not callable
        :raise TypeError: if 'result_transform' is not callable
        """
        if not isinstance(other, Iterable):
            raise TypeError("Value for 'other' is not an Iterable.")
        if not callable(key_selector):
            raise TypeError("Value for 'key_selector' is not callable.")
        if not callable(other_key_selector):
            raise TypeError("Value for 'other_key_selector' is not callable.")
        if not callable(result_transform):
            raise TypeError("Value for 'result_transform' is not callable.")

        @lru_cache(1, False)
        def _other_groups():
            groups = defaultdict(list)
            for element in other:
                key = other_key_selector(element)
                groups[key].append(element)
            return groups
        if result_transform.__code__.co_argcount == 1:
            return Queryable((result_transform(element) for element in chain.from_iterable(
                ([(element, other_element) for other_element in _other_groups()[
                    key_selector(element)]] for element in self))))
        else:
            return Queryable((result_transform(*element) for element in chain.from_iterable(
                ([(element, other_element) for other_element in _other_groups()[
                    key_selector(element)]] for element in self))))

    def last(self, predicate=true):
        """Returns the last item of the sequence.

        :param predicate: (optional) A function to test each element for a condition.
        :type predicate: function
        :return: The last item in the sequence that satisfies the condition.
        :raise TypeError: if 'predicate' is not callable
        :raise ValueError: if the source iterable is empty
        :raise ValueError: if no element satisfies condition
        """
        if not callable(predicate):
            raise TypeError("Value for 'predicate' is not callable.")
        last_element = None
        found_element = False
        count = 0
        for element in self:
            count += 1
            if predicate(element):
                found_element = True
                last_element = element
        if found_element:
            return last_element
        if count == 0:
            raise ValueError("The source sequence is empty.")
        raise ValueError("No element satisfies the predicate.")

    def last_or_default(self, predicate=true, default_value=None):
        """Returns the last item of the sequence.

        :param predicate: (optional) A function to test each element for a condition.
        :type predicate: function
        :param default_value: (optional) The default value to return if empty.
        :return: The last item in the sequence that satisfies the condition.
        :raise TypeError: if 'predicate' is not callable
        :raise ValueError: if the source iterable is empty
        :raise ValueError: if no element satisfies condition
        """
        if not callable(predicate):
            raise TypeError("Value for 'predicate' is not callable.")
        last_element = default_value
        count = 0
        for element in self:
            count += 1
            if predicate(element):
                last_element = element
        return last_element

    def long_count(self, predicate=true):
        """Returns the number of elements in the sequence.

        :param predicate: (optional) A function to test each element for a condition:
        :type predicate: function
        :return: The number of elements that satisfy the specified condition.
        :rtype: int
        :raise TypeError: if 'predicate' is not callable
        """
        if not callable(predicate):
            raise TypeError("Value for 'predicate' is not callable.")
        count = 0
        for element in self:
            if predicate(element):
                count += 1
        return count

    def max(self, transform=identity):
        """Returns the maximum element in the sequence.

        :param transform: (optional) A transformation function to apply to each element.
        :type transform: function
        :return: The maximum element in the sequence.
        :rtype: int
        :raise TypeError: if 'transform' is not callable
        """
        if not callable(transform):
            raise TypeError("Value for 'transform' is not callable.")
        return max((transform(element) for element in self))

    def min(self, transform=identity):
        """Returns the minimum element in the sequence.

        :param transform: (optional) A transformation function to apply to each element.
        :type transform: function
        :return: The minimum element in the sequence.
        :rtype: int
        :raise TypeError: if 'transform' is not callable
        """
        if not callable(transform):
            raise TypeError("Value for 'transform' is not callable.")
        return min((transform(element) for element in self))

    def of_type(self, of_type):
        """Filters the elements based on the specified type.

        :param of_type: The type to keep.
        :type of_type: type
        :return: The elements of the sequence with the specified type.
        :rtype: :class:`Queryable`
        :raise TypeError: if 'of_type' is not a type
        """
        if not isinstance(of_type, type):
            raise TypeError("Value for 'of_type' is not a type.")
        return Queryable((element for element in self if isinstance(element, of_type)))

    def order_by(self, key_selector):
        """Sorts the elements of the sequence in ascending order according to a key.

        :param key_selector: A function to extract a key from an element.
        :type key_selector: function
        :return: The elements of the sequence sorted in ascending order.
        :rtype: :class:`OrderedQueryable`
        :raise TypeError: if 'key_selector' is not callable
        """
        if not callable(key_selector):
            raise TypeError("Value for 'key_selector' is not callable.")
        return OrderedQueryable(self, [(key_selector, False)])

    def order_by_descending(self, key_selector):
        """Sorts the elements of the sequence in descending order according to a key.

        :param key_selector: A function to extract a key from an element.
        :type key_selector: function
        :return: The elements of the sequence sorted in descending order.
        :rtype: :class:`OrderedQueryable`
        :raise TypeError: if 'key_selector' is not callable
        """
        if not callable(key_selector):
            raise TypeError("Value for 'key_selector' is not callable.")
        return OrderedQueryable(self, [(key_selector, True)])

    def reverse(self):
        """Reverses the order of the elements in the sequence.

        :return: The elements of the sequence in reverse order.
        :rtype: :class:`Queryable`
        """
        def _reverse(iterator):
            elements = []
            for element in iterator:
                elements.append(element)
            while len(elements) > 0:
                yield elements.pop()
        return Queryable(_reverse(self))

    def select(self, selector):
        """Returns the elements of the sequence after applying a transform function to each element.

        :param selector: A transform function to apply to each element.
        :type selector: function
        :return: The elements of the sequence after applying the transform function.
        :rtype: :class:`Queryable`
        :raise TypeError: if 'selector' is not callable
        """
        if not callable(selector):
            raise TypeError("Value for 'selector' is not callable.")
        if selector.__code__.co_argcount == 1:
            return Queryable((selector(element) for element in self))
        else:
            return Queryable((selector(element, index) for index, element in enumerate(self)))

    def select_many(self, selector, result_transform=select_i(1)):
        """Projects each element to a sequence and flattens the resulting sequences.

        :param selector: A function to transform each element into a sequence.
        :type selector: function
        :param result_transform: (optional) A transform function for items of the selected sequence.
        :type result_transform: function
        :return: A flattened sequence of transformed elements.
        :rtype: :class:`Queryable`
        :raise TypeError: if 'selector' is not callable
        :raise TypeError: if 'result_transform' is not callable
        """
        if not callable(selector):
            raise TypeError("Value for 'selector' is not callable.")
        if not callable(result_transform):
            raise TypeError("Value for 'result_transform' is not callable.")
        if selector.__code__.co_argcount == 1:
            return Queryable(chain.from_iterable(([result_transform(
                element, sub_element) for sub_element in selector(element)] for element in self)))
        else:
            return Queryable(chain.from_iterable(([result_transform(
                element, sub_element) for sub_element in selector(
                    element, index)] for index, element in enumerate(self))))

    def sequence_equal(self, other, equality_comparer=eq):
        """Determines whether two sequences are equal.

        :param other: The sequence to compare elements to.
        :type other: Iterable
        :param equality_comparer: (optional) The equality comparison function to use.
        :type equality_comparer: function
        :return: True if the sequences are equal, false otherwise.
        :rtype: bool
        :raise TypeError: if 'other' is not an Iterable
        :raise TypeError: if 'equality_comparer' is not callable
        """
        if not isinstance(other, Iterable):
            raise TypeError("Value for 'other' is not an Iterable.")
        if not callable(equality_comparer):
            raise TypeError("Value for 'equality_comparer' is not callable.")

        class _IterableEnd:
            pass
        for element1, element2 in zip_longest(self, other, fillvalue=_IterableEnd()):
            if isinstance(element1, _IterableEnd) or isinstance(element2, _IterableEnd):
                return False
            elif not equality_comparer(element1, element2):
                return False
        return True

    def single(self, predicate=true):
        """Returns the only element of the sequence.

        :param predicate: (optional) A function to test an element for a condition.
        :type predicate: function
        :return: The single element of the sequence satisfying the condition.
        :raise TypeError: if 'predicate' is not callable
        :raise ValueError: if the sequence is empty
        :raise ValueError: if no element satisfies the condition
        :raise ValueError: if more than one element satisfies the condition
        """
        if not callable(predicate):
            raise TypeError("Value for 'predicate' is not callable.")

        class _NoItem:
            pass
        single_item = _NoItem()
        count = 0
        for element in self:
            count += 1
            if predicate(element):
                if not isinstance(single_item, _NoItem):
                    raise ValueError(
                        "More than one element satisfies 'predicate'.")
                single_item = element
        if not isinstance(single_item, _NoItem):
            return single_item
        if count == 0:
            raise ValueError("The source sequence is empty.")
        raise ValueError("More than one element satisfies 'predicate'.")

    def single_or_default(self, predicate=true, default_value=None):
        """Returns the only element of the sequence.

        :param predicate: (optional) A function to test an element for a condition.
        :type predicate: function
        :param default_value: (optional) The default value to return if empty.
        :return: The single element of the sequence satisfying the condition.
        :raise TypeError: if 'predicate' is not callable
        :raise ValueError: if more than one element satisfies the condition
        """
        if not callable(predicate):
            raise TypeError("Value for 'predicate' is not callable.")

        class _NoItem:
            pass
        single_item = _NoItem()
        count = 0
        for element in self:
            count += 1
            if predicate(element):
                if not isinstance(single_item, _NoItem):
                    raise ValueError(
                        "More than one element satisfies 'predicate'.")
                single_item = element
        if not isinstance(single_item, _NoItem):
            return single_item
        return default_value

    def skip(self, num):
        """Skips a specified number of elements in the sequence and returns the remaining elements.

        :param num: The number of elements to skip.
        :type num: int
        :return: A sequence containing the elements after position 'num'.
        :rtype: :class:`Queryable`
        :raise TypeError: if 'num' is not an int
        """
        if not isinstance(num, int):
            raise TypeError("Value for 'num' is not an integer.")
        return Queryable(islice(self, num, None))

    def skip_while(self, predicate):
        """Skip elements of the sequence while the specified condition is true.

        :param predicate: The condition to check for.
        :type predicate: function
        :return: Elements of the sequence after the first item to fail the specified condition.
        :rtype: :class:`Queryable`
        :raise TypeError: if 'condition' is not callable
        """
        if not callable(predicate):
            raise TypeError("Value for 'predicate' is not callable.")
        return Queryable(dropwhile(predicate, self))

    def sum(self, transform=identity):
        """Computes the sum of the sequence by invoking a transform on each element.

        :param transform: (optional) A transform function to apply to each element.
        :type transform: function
        :return: The sum of the elements of the sequence.
        :rtype: int
        :raise TypeError: if 'transform' is not callable
        """
        if not callable(transform):
            raise TypeError("Value for 'transform' is not callable.")
        return sum((transform(element) for element in self))

    def take(self, num):
        """Takes the specified number of elements from the start of the sequence.

        :param num: The number of elements to take.
        :type num: int
        :return: The specified number of elements from the start of the sequence.
        :rtype: :class:`Queryable`
        :raise TypeError: if 'num' is not an int
        """
        if not isinstance(num, int):
            raise TypeError("Value for 'num' is not an integer.")
        return Queryable(islice(self, num))

    def take_while(self, predicate):
        """Takes elements from the start of the sequence while the specified condition holds.

        :param predicate: The condition to check for.
        :type predicate: function
        :return: The elements from the start of the sequence that satisfy the condition.
        :rtype: :class:`Queryable`
        :raise TypeError: if 'predicate' is not callable
        """
        if not callable(predicate):
            raise TypeError("Value for 'predicate' is not callable.")
        return Queryable(takewhile(predicate, self))

    def to_dict(self, key_selector, value_selector=identity):
        """Creates a dictionary object according to the specified key selector function.

        :param key_selector: A function to extract the key for the dictionary entry.
        :type key_selector: function
        :param value_selector: (optional) A function to extract the value for the dictionary entry.
        :type value_selector: function
        :return: A dictionary of the elements in the sequence.
        :rtype: dict
        :raise TypeError: if 'key_selector' is not callable
        :raise TypeError: if 'value_selector' is not callable
        """
        return self.to_dictionary(key_selector, value_selector)

    def to_dictionary(self, key_selector, value_selector=identity):
        """Creates a dictionary object according to the specified key selector function.

        :param key_selector: A function to extract the key for the dictionary entry.
        :type key_selector: function
        :param value_selector: (optional) A function to extract the value for the dictionary entry.
        :type value_selector: function
        :return: A dictionary of the elements in the sequence.
        :rtype: dict
        :raise TypeError: if 'key_selector' is not callable
        :raise TypeError: if 'value_selector' is not callable
        """
        if not callable(key_selector):
            raise TypeError(
                "Value for 'key_selector' is not callable.")
        if not callable(value_selector):
            raise TypeError(
                "Value for 'value_selector' is not callable.")
        return dict(((key_selector(element), value_selector(element)) for element in self))

    def to_list(self):
        """Creates a list object from the sequence.

        :return: A list of the elements in the sequence.
        :rtype: list
        """
        return list(self)

    def union(self, other, key_selector=identity):
        """Returns the set union of two sequences.

        :param other: The second sequence to produce the union with.
        :type other: Iterable
        :param key_selector: (optional) A function to extract a key for comparison.
        :type key_selector: function
        :return: The set union of the two sequences.
        :rtype: :class:`Queryable`
        :raise TypeError: if 'other' is not an Iterable
        :raise TypeError: if 'key_selector' is not callable
        """
        if not isinstance(other, Iterable):
            raise TypeError("Value for 'other' is not an Iterable.")
        if not callable(key_selector):
            raise TypeError("Value for 'key_selector' is not callable.")
        seen = {}

        def _seen(value):
            key = key_selector(value)
            if key in seen:
                return True
            seen[key] = 1
            return False
        return Queryable((element for element in chain(self, other) if not _seen(element)))

    def where(self, predicate):
        """Filters the sequence of values based on the specified condition.

        :param predicate: A function to check an element for a condition.
        :type condition: function
        :return: The elements of the sequence that satisfy the condition.
        :rtype: :class:`Queryable`
        :raise TypeError: if 'predicate' is not callable
        """
        if not callable(predicate):
            raise TypeError("Value for 'predicate' is not callable.")
        if predicate.__code__.co_argcount == 1:
            return Queryable((element for element in self if predicate(element)))
        else:
            return Queryable(
                (element for index, element in enumerate(self) if predicate(element, index)))

    def zip(self, other, result_transform):
        """Applies a function to the corresponding elements of the two sequences.

        :param other: The other input sequence.
        :type other: Iterable
        :param result_transform: A function that combines the corresponding elements.
        :type result_transform: function
        :return: A sequence of elements of the two sequences combined using 'result_transform'.
        :rtype: :class:`Queryable`
        :raise TypeError: if 'other' is not an Iterable
        :raise TypeError: if 'result_transform' is not callable
        """
        if not isinstance(other, Iterable):
            raise TypeError("Value for 'other' is not an Iterable.")
        if not callable(result_transform):
            raise TypeError("Value for 'result_transform' is not callable.")
        return Queryable((result_transform(*element) for element in zip(self, other)))


class OrderedQueryable(Queryable):
    """A wrapper for ordered sequences.
    """

    def __init__(self, iterator, keys):
        super(OrderedQueryable, self).__init__(iterator)
        self._keys = keys

    def __iter__(self):
        sorted_elements = self.iterator
        for key_selector in self._keys:
            sorted_elements = sorted(sorted_elements, key=key_selector[
                0], reverse=key_selector[1])
        for element in sorted_elements:
            yield element

    def then_by(self, key_selector):
        """Performs a subsequenct ordering on the elements of an ordered sequence.

        :param key: A function to extract a key to use for comparisons.
        :type key: function
        :return: The elements of the sequence in ascending order according to the key
        :rtype: :class:`Queryable`
        :raise TypeError: if 'key_selector' is not callable
        """
        if not callable(key_selector):
            raise TypeError("Value for 'key_selector' is not callable.")
        self._keys.insert(0, (key_selector, False))
        return self

    def then_by_descending(self, key_selector):
        """Performs a subsequenct ordering on the elements of an ordered sequence.

        :param key: A function to extract a key to use for comparisons.
        :type key: function
        :return: The elements of the sequence in descending order according to the key
        :rtype: :class:`Queryable`
        :raise TypeError: if 'key_selector' is not callable
        """
        if not callable(key_selector):
            raise TypeError("Value for 'key_selector' is not callable.")
        self._keys.insert(0, (key_selector, True))
        return self
