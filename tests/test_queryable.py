"""
Tests for queryables.
"""

import unittest
import pylinq


def generator(num):
    for i in range(num):
        yield i


class queryable_tests(unittest.TestCase):

    def setUp(self):
        self.queryable_1 = pylinq.as_queryable([])
        self.queryable_2 = pylinq.as_queryable([1, 3, 5, 9, 10, 13, 7, 2])
        self.queryable_3 = pylinq.as_queryable([i for i in range(1000)])
        self.queryable_4 = pylinq.as_queryable(
            ([1, 2, 3], [3, 4, 5], [2, 8, 10]))
        self.queryable_5 = pylinq.as_queryable([[1, 2, 3], [1, 4, 5], [4, 4, 4], [
            1, 1, 9], [4, 3, 2], [9, 5, 7], [8, 6, 2], [9, 4, 5]])
        self.queryable_6 = pylinq.as_queryable(
            [[1, [1, 2, 3]], [2, [4, 5, 6]], [3, [7, 8, 9]]])
        self.queryable_7 = pylinq.as_queryable(generator(1000000))

    def test_multiple_enumerate(self):
        self.assertEqual(self.queryable_7.where(
            lambda x: x == 7).to_list(), [7])
        self.assertEqual(self.queryable_7.where(
            lambda x: x == 8).to_list(), [8])
        self.assertEqual(self.queryable_7.where(
            lambda x: x == 15).to_list(), [15])
        self.assertEqual(self.queryable_7.where(
            lambda x: x % 2 == 0).select(lambda x: x / 2).to_list(), [i for i in range(500000)])
        self.assertEqual(self.queryable_7.where(
            lambda x: x % 2 == 0).to_list(), [i * 2 for i in range(500000)])

    def test_aggregate(self):
        self.assertEqual(self.queryable_2.aggregate(lambda x, y: x + y), 50)
        self.assertEqual(self.queryable_4.aggregate(
            lambda x, y: x + y[1], 0), 14)
        self.assertEqual(self.queryable_4.aggregate(
            lambda x, y: x + y, [], lambda x: x[0]), 1)
        with self.assertRaises(TypeError):
            self.queryable_2.aggregate(40)
        with self.assertRaises(TypeError):
            self.queryable_2.aggregate(lambda x, y: x + y, 0, 100)

    def test_all(self):
        self.assertTrue(self.queryable_1.all(lambda x: x < 100))
        self.assertTrue(self.queryable_2.all(lambda x: x < 100))
        self.assertFalse(self.queryable_2.all(lambda x: x < 10))
        self.assertTrue(self.queryable_3.all(lambda x: x >= 0))
        self.assertFalse(self.queryable_3.all(lambda x: x < 10))
        with self.assertRaises(TypeError):
            self.queryable_2.all(100)

    def test_any(self):
        self.assertFalse(self.queryable_1.any(lambda x: x < 100))
        self.assertTrue(self.queryable_2.any(lambda x: x < 10))
        self.assertFalse(self.queryable_2.any(lambda x: x < 0))
        self.assertFalse(self.queryable_3.any(lambda x: x < 0))
        self.assertTrue(self.queryable_3.any(lambda x: x < 10))
        self.assertFalse(self.queryable_1.any())
        with self.assertRaises(TypeError):
            self.queryable_2.any(100)

    def test_average(self):
        transform = lambda x: x[0]
        self.assertEqual(self.queryable_2.average(), 6.25)
        self.assertEqual(self.queryable_4.average(transform), 2.0)
        with self.assertRaises(TypeError):
            self.queryable_2.average(5)
        with self.assertRaises(ZeroDivisionError):
            self.queryable_1.average()

    def test_cast(self):
        self.assertEqual(list(self.queryable_1.cast(str)), [])
        self.assertEqual(list(self.queryable_2.cast(str)), [
            "1", "3", "5", "9", "10", "13", "7", "2"])
        with self.assertRaises(TypeError):
            self.queryable_3.cast(lambda x: x - 1)

    def test_concat(self):
        self.assertEqual(list(self.queryable_1.concat(self.queryable_2)), [
            1, 3, 5, 9, 10, 13, 7, 2])
        self.assertEqual(list(self.queryable_1.concat([1, 2, 3])), [1, 2, 3])
        with self.assertRaises(TypeError):
            self.queryable_1.concat(200)

    def test_contains(self):
        comparer = lambda x1, x2: x1[0] == x2[0]
        self.assertFalse(self.queryable_1.contains(100))
        self.assertTrue(self.queryable_2.contains(7))
        self.assertTrue(self.queryable_4.contains([2], comparer))
        with self.assertRaises(TypeError):
            self.queryable_1.contains(7, "equal")

    def test_count(self):
        condition = lambda x: x < 7
        self.assertEqual(self.queryable_1.count(), 0)
        self.assertEqual(self.queryable_3.count(), 1000)
        self.assertEqual(self.queryable_4.count(), 3)
        self.assertEqual(self.queryable_2.count(condition), 4)
        with self.assertRaises(TypeError):
            self.queryable_1.count(3)

    def test_default_if_empty(self):
        self.assertEqual(list(self.queryable_1.default_if_empty()), [None])
        self.assertEqual(list(self.queryable_2.default_if_empty()),
                         [1, 3, 5, 9, 10, 13, 7, 2])

    def test_difference(self):
        self.assertEqual(
            list(self.queryable_1.difference(self.queryable_2)), [])
        self.assertEqual(list(self.queryable_2.difference(
            self.queryable_1)), [1, 3, 5, 9, 10, 13, 7, 2])
        self.assertEqual(list(self.queryable_4.difference(
            self.queryable_2, lambda x: x[0], lambda x: x)), [])
        self.assertEqual(list(self.queryable_4.difference(
            self.queryable_2, lambda x: x[1], lambda x: x)), [[3, 4, 5], [2, 8, 10]])
        self.assertEqual(list(self.queryable_5.difference(
            self.queryable_4, lambda x: x[0])), [[4, 4, 4], [9, 5, 7], [8, 6, 2]])
        with self.assertRaises(TypeError):
            self.queryable_1.difference(0)
        with self.assertRaises(TypeError):
            self.queryable_1.difference(self.queryable_1, 0)
        with self.assertRaises(TypeError):
            self.queryable_1.difference(self.queryable_1, lambda x: x, 0)

    def test_distinct(self):
        self.assertEqual(list(self.queryable_1.distinct()), [])
        self.assertEqual(list(self.queryable_2.distinct()),
                         [1, 3, 5, 9, 10, 13, 7, 2])
        self.assertEqual(list(self.queryable_5.distinct(
            lambda x: x[0])), [[1, 2, 3], [4, 4, 4], [9, 5, 7], [8, 6, 2]])
        with self.assertRaises(TypeError):
            self.queryable_2.distinct(100)

    def test_element_at(self):
        self.assertEqual(self.queryable_2.element_at(3), 9)
        self.assertEqual(self.queryable_2.element_at(-1), 2)
        with self.assertRaises(TypeError):
            self.queryable_2.element_at("1")
        with self.assertRaises(IndexError):
            self.queryable_1.element_at(1)

    def test_element_at_or_default(self):
        self.assertEqual(self.queryable_2.element_at_or_default(3), 9)
        self.assertEqual(self.queryable_2.element_at_or_default(-1), 2)
        self.assertEqual(self.queryable_1.element_at_or_default(1), None)
        with self.assertRaises(TypeError):
            self.queryable_2.element_at_or_default("1")

    def test_empty(self):
        self.assertTrue(self.queryable_1.empty())
        self.assertFalse(self.queryable_4.empty())

    def test_first(self):
        condition = lambda x: x > 200
        self.assertEqual(self.queryable_3.first(condition), 201)
        self.assertEqual(self.queryable_4.first(), [1, 2, 3])
        with self.assertRaises(TypeError):
            self.queryable_2.first(13)
        with self.assertRaises(ValueError):
            self.queryable_1.first()
        with self.assertRaises(ValueError):
            self.queryable_2.first(lambda x: x > 1000)

    def test_first_or_default(self):
        condition = lambda x: x > 200
        self.assertEqual(self.queryable_3.first_or_default(condition), 201)
        self.assertEqual(self.queryable_4.first_or_default(), [1, 2, 3])
        self.assertEqual(self.queryable_1.first_or_default(), None)
        with self.assertRaises(TypeError):
            self.queryable_2.first_or_default(13)

    def test_group_by(self):
        key1 = lambda x: x[0]
        selectKey = lambda x: x[0]
        selectValues = lambda x: x[1]
        self.assertEqual(list(self.queryable_4.group_by(
            key1).select(selectKey)), [1, 2, 3])
        self.assertEqual(list(self.queryable_4.group_by(
            key1).select_many(selectValues)), [[1, 2, 3], [2, 8, 10], [3, 4, 5]])
        self.assertEqual(list(self.queryable_5.group_by(
            key1).select(selectKey)), [1, 4, 8, 9])
        self.assertEqual(list(self.queryable_5.group_by(
            key1).select_many(selectValues)), [[1, 2, 3], [1, 4, 5], [1, 1, 9], [
                4, 4, 4], [4, 3, 2], [8, 6, 2], [9, 5, 7], [9, 4, 5]])
        with self.assertRaises(TypeError):
            self.queryable_2.group_by(100)

    def test_group_join(self):
        key1 = lambda x: x[0]
        key2 = lambda x: x[1]
        joiner = lambda x, g: x + list(g)
        self.assertEqual(list(self.queryable_4.group_join(self.queryable_5, key1, key2, joiner)), [
            [1, 2, 3, [1, 1, 9]], [2, 8, 10, [1, 2, 3]], [3, 4, 5, [4, 3, 2]]])
        self.assertEqual(list(self.queryable_4.group_join(self.queryable_5, key1, key1, joiner)), [
            [1, 2, 3, [1, 2, 3], [1, 4, 5], [1, 1, 9]]])
        self.assertEqual(list(self.queryable_5.group_join(self.queryable_4, key1, key1, joiner)), [
            [1, 2, 3, [1, 2, 3]], [1, 4, 5, [1, 2, 3]], [1, 1, 9, [1, 2, 3]]])
        with self.assertRaises(TypeError):
            self.queryable_1.group_join(0, key1, key2, joiner)
        with self.assertRaises(TypeError):
            self.queryable_4.group_join(self.queryable_4, 0, key2, joiner)
        with self.assertRaises(TypeError):
            self.queryable_4.group_join(self.queryable_4, key1, 0, joiner)
        with self.assertRaises(TypeError):
            self.queryable_4.group_join(self.queryable_4, key1, key2, 0)

    def test_intersect(self):
        key1 = lambda x: x
        key2 = lambda x: x[0]
        self.assertEqual(
            list(self.queryable_1.intersect(self.queryable_2)), [])
        self.assertEqual(list(self.queryable_2.intersect(
            self.queryable_2)), [1, 3, 5, 9, 10, 13, 7, 2])
        self.assertEqual(list(self.queryable_3.intersect(
            self.queryable_2)), [1, 2, 3, 5, 7, 9, 10, 13])
        self.assertEqual(list(self.queryable_4.intersect(
            self.queryable_5, key2)), [[1, 2, 3]])
        self.assertEqual(list(self.queryable_2.intersect(
            self.queryable_4, key1, key2)), [1, 3, 2])
        self.assertEqual(list(self.queryable_7.select(
            lambda x: x % 5).intersect(self.queryable_1)), [])
        with self.assertRaises(TypeError):
            self.queryable_1.intersect(100)
        with self.assertRaises(TypeError):
            self.queryable_2.intersect(self.queryable_2, 0)
        with self.assertRaises(TypeError):
            self.queryable_2.intersect(self.queryable_2, key1, 0)

    def test_join(self):
        key1 = lambda x: x[0]
        key2 = lambda x: x[1]
        joiner = lambda x, y: x + y
        self.assertEqual(list(self.queryable_4.join(self.queryable_5, key1, key2, joiner)), [
            [1, 2, 3, 1, 1, 9], [2, 8, 10, 1, 2, 3], [3, 4, 5, 4, 3, 2]])
        self.assertEqual(list(self.queryable_4.join(self.queryable_5, key1, key1, joiner)), [
            [1, 2, 3, 1, 2, 3], [1, 2, 3, 1, 4, 5], [1, 2, 3, 1, 1, 9]])
        self.assertEqual(list(self.queryable_5.join(self.queryable_4, key1, key1, joiner)), [
            [1, 2, 3, 1, 2, 3], [1, 4, 5, 1, 2, 3], [1, 1, 9, 1, 2, 3]])
        with self.assertRaises(TypeError):
            self.queryable_1.join(0, key1, key2, joiner)
        with self.assertRaises(TypeError):
            self.queryable_4.join(self.queryable_4, 0, key2, joiner)
        with self.assertRaises(TypeError):
            self.queryable_4.join(self.queryable_4, key1, 0, joiner)
        with self.assertRaises(TypeError):
            self.queryable_4.join(self.queryable_4, key1, key2, 0)

    def test_last(self):
        condition = lambda x: x < 400
        self.assertEqual(self.queryable_3.last(condition), 399)
        self.assertEqual(self.queryable_4.last(), [2, 8, 10])
        with self.assertRaises(TypeError):
            self.queryable_2.last(13)
        with self.assertRaises(ValueError):
            self.queryable_1.last()
        with self.assertRaises(ValueError):
            self.queryable_2.last(lambda x: x > 1000)

    def test_last_or_default(self):
        condition = lambda x: x < 400
        self.assertEqual(self.queryable_3.last_or_default(condition), 399)
        self.assertEqual(self.queryable_4.last_or_default(), [2, 8, 10])
        self.assertEqual(self.queryable_1.last_or_default(), None)
        with self.assertRaises(TypeError):
            self.queryable_2.last_or_default(13)

    def test_long_count(self):
        condition = lambda x: x < 7
        self.assertEqual(self.queryable_1.long_count(), 0)
        self.assertEqual(self.queryable_3.long_count(), 1000)
        self.assertEqual(self.queryable_4.long_count(), 3)
        self.assertEqual(self.queryable_2.long_count(condition), 4)
        with self.assertRaises(TypeError):
            self.queryable_1.long_count(3)

    def test_max(self):
        transform = lambda x: x if x < 7 else x - 7
        self.assertEqual(self.queryable_2.max(), 13)
        self.assertEqual(self.queryable_2.max(transform), 6)
        with self.assertRaises(TypeError):
            self.queryable_2.max(4)
        with self.assertRaises(ValueError):
            self.queryable_1.max()

    def test_min(self):
        transform = lambda x: x if x < 7 else x - 7
        self.assertEqual(self.queryable_2.min(), 1)
        self.assertEqual(self.queryable_2.min(transform), 0)
        with self.assertRaises(TypeError):
            self.queryable_2.min(4)
        with self.assertRaises(ValueError):
            self.queryable_1.min()

    def test_of_type(self):
        self.assertEqual(list(self.queryable_2.of_type(int)),
                         [1, 3, 5, 9, 10, 13, 7, 2])
        with self.assertRaises(TypeError):
            self.queryable_2.of_type("string")

    def test_order_by(self):
        self.assertEqual(list(self.queryable_1.order_by(lambda x: x)), [])
        self.assertEqual(list(self.queryable_2.order_by(lambda x: x)), [
            1, 2, 3, 5, 7, 9, 10, 13])
        self.assertEqual(list(self.queryable_4.order_by(lambda x: x[0])), [
            [1, 2, 3], [2, 8, 10], [3, 4, 5]])
        with self.assertRaises(TypeError):
            self.queryable_2.order_by(2)

    def test_order_by_descending(self):
        self.assertEqual(
            list(self.queryable_1.order_by_descending(lambda x: x)), [])
        self.assertEqual(list(self.queryable_2.order_by_descending(lambda x: x)), [
            13, 10, 9, 7, 5, 3, 2, 1])
        self.assertEqual(list(self.queryable_4.order_by_descending(
            lambda x: x[0])), [[3, 4, 5], [2, 8, 10], [1, 2, 3]])
        with self.assertRaises(TypeError):
            self.queryable_2.order_by_descending(2)

    def test_reverse(self):
        self.assertEqual(list(self.queryable_1.reverse()), [])
        self.assertEqual(list(self.queryable_2.reverse()),
                         [2, 7, 13, 10, 9, 5, 3, 1])
        self.assertEqual(list(self.queryable_4.reverse()), [
                         [2, 8, 10], [3, 4, 5], [1, 2, 3]])

    def test_select(self):
        selector1 = str
        selector2 = lambda x: x[-1]
        self.assertEqual(list(self.queryable_1.select(selector1)), [])
        self.assertEqual(list(self.queryable_2.select(selector1)), [
            "1", "3", "5", "9", "10", "13", "7", "2"])
        self.assertEqual(list(self.queryable_4.select(selector2)), [3, 5, 10])
        with self.assertRaises(TypeError):
            self.queryable_1.select(3)

    def test_select_many(self):
        selector1 = lambda x: x[1]
        self.assertEqual(list(self.queryable_6.select_many(selector1)), [
            1, 2, 3, 4, 5, 6, 7, 8, 9])
        with self.assertRaises(TypeError):
            self.queryable_6.select_many(41)

    def test_sequence_equal(self):
        self.assertTrue(self.queryable_1.sequence_equal([]))
        self.assertTrue(self.queryable_2.sequence_equal(
            [1, 3, 5, 9, 10, 13, 7, 2]))
        self.assertTrue(self.queryable_2.sequence_equal(self.queryable_2))
        self.assertFalse(self.queryable_2.sequence_equal(self.queryable_3))
        with self.assertRaises(TypeError):
            self.queryable_2.sequence_equal(100)
        self.assertTrue(self.queryable_4.sequence_equal(
            [1, 3, 2], comparer=lambda x, y: x[0] == y))
        self.assertFalse(self.queryable_4.sequence_equal(
            [10, 40, 20], comparer=lambda x, y: x[0] == y))
        with self.assertRaises(TypeError):
            self.queryable_4.sequence_equal([1, 2, 3], comparer=100)

    def test_single(self):
        condition = lambda x: 1 in x
        self.assertEqual(self.queryable_4.single(condition), [1, 2, 3])
        with self.assertRaises(ValueError):
            self.queryable_1.single()
        with self.assertRaises(ValueError):
            self.queryable_2.single()
        with self.assertRaises(ValueError):
            self.queryable_2.single(lambda x: x > 30)
        with self.assertRaises(TypeError):
            self.queryable_2.single(100)

    def test_single_or_default(self):
        condition = lambda x: 1 in x
        self.assertEqual(
            self.queryable_4.single_or_default(condition), [1, 2, 3])
        self.assertEqual(self.queryable_1.single_or_default(), None)
        with self.assertRaises(ValueError):
            self.queryable_2.single_or_default()
        with self.assertRaises(ValueError):
            self.queryable_2.single_or_default(lambda x: x > 3)
        with self.assertRaises(TypeError):
            self.queryable_2.single_or_default(100)

    def test_skip(self):
        self.assertEqual(list(self.queryable_1.skip(5)), [])
        self.assertEqual(list(self.queryable_2.skip(5)), [13, 7, 2])
        with self.assertRaises(TypeError):
            self.queryable_3.skip("all")

    def test_skip_while(self):
        condition = lambda x: x < 10
        self.assertEqual(list(self.queryable_1.skip_while(condition)), [])
        self.assertEqual(
            list(self.queryable_2.skip_while(condition)), [10, 13, 7, 2])
        with self.assertRaises(TypeError):
            self.queryable_3.skip_while("all")

    def test_sum(self):
        transform = lambda x: x - 7
        self.assertEqual(self.queryable_1.sum(), 0)
        self.assertEqual(self.queryable_2.sum(), 50)
        self.assertEqual(self.queryable_2.sum(transform), -6)
        with self.assertRaises(TypeError):
            self.queryable_3.sum(100)

    def test_take(self):
        self.assertEqual(list(self.queryable_1.take(5)), [])
        self.assertEqual(list(self.queryable_2.take(5)), [1, 3, 5, 9, 10])
        with self.assertRaises(TypeError):
            self.queryable_3.take("all")

    def test_take_while(self):
        condition = lambda x: x < 10
        self.assertEqual(list(self.queryable_1.take_while(condition)), [])
        self.assertEqual(
            list(self.queryable_2.take_while(condition)), [1, 3, 5, 9])
        with self.assertRaises(TypeError):
            self.queryable_3.take_while("all")

    def test_then_by(self):
        key1 = lambda x: x[0]
        key2 = lambda x: x[1]
        self.assertEqual(list(self.queryable_5.order_by(key1)), [[1, 2, 3], [1, 4, 5], [
            1, 1, 9], [4, 4, 4], [4, 3, 2], [8, 6, 2], [9, 5, 7], [9, 4, 5]])
        self.assertEqual(list(self.queryable_5.order_by_descending(key1)), [[9, 5, 7], [
            9, 4, 5], [8, 6, 2], [4, 4, 4], [4, 3, 2], [1, 2, 3], [1, 4, 5], [1, 1, 9]])
        self.assertEqual(list(self.queryable_5.order_by(key1).then_by(key2)), [[1, 1, 9], [
            1, 2, 3], [1, 4, 5], [4, 3, 2], [4, 4, 4], [8, 6, 2], [9, 4, 5], [9, 5, 7]])
        self.assertEqual(list(self.queryable_5.order_by_descending(key1).then_by(key2)), [
            [9, 4, 5], [9, 5, 7], [8, 6, 2], [4, 3, 2], [4, 4, 4], [1, 1, 9], [1, 2, 3], [1, 4, 5]])
        with self.assertRaises(TypeError):
            self.queryable_5.order_by(key1).then_by(100)
        with self.assertRaises(ValueError):
            self.queryable_5.then_by(key2)

    def test_then_by_descending(self):
        key1 = lambda x: x[0]
        key2 = lambda x: x[1]
        self.assertEqual(list(self.queryable_5.order_by(key1)), [[1, 2, 3], [1, 4, 5], [
            1, 1, 9], [4, 4, 4], [4, 3, 2], [8, 6, 2], [9, 5, 7], [9, 4, 5]])
        self.assertEqual(list(self.queryable_5.order_by_descending(key1)), [[9, 5, 7], [
            9, 4, 5], [8, 6, 2], [4, 4, 4], [4, 3, 2], [1, 2, 3], [1, 4, 5], [1, 1, 9]])
        self.assertEqual(list(self.queryable_5.order_by(key1).then_by_descending(key2)), [
            [1, 4, 5], [1, 2, 3], [1, 1, 9], [4, 4, 4], [4, 3, 2], [8, 6, 2], [9, 5, 7], [9, 4, 5]])
        self.assertEqual(list(self.queryable_5.order_by_descending(key1).then_by_descending(key2)),
                         [[9, 5, 7], [9, 4, 5], [8, 6, 2], [4, 4, 4], [4, 3, 2], [1, 4, 5],
                          [1, 2, 3], [1, 1, 9]])
        with self.assertRaises(TypeError):
            self.queryable_5.order_by(key1).then_by_descending(100)
        with self.assertRaises(ValueError):
            self.queryable_5.then_by_descending(key2)

    def test_to_dictionary(self):
        self.assertDictEqual(self.queryable_1.to_dictionary(lambda x: x), {})
        self.assertDictEqual(self.queryable_2.to_dictionary(
            lambda x: x * x), {1: 1, 9: 3, 25: 5, 81: 9, 100: 10, 169: 13, 49: 7, 4: 2})
        self.assertDictEqual(self.queryable_2.to_dictionary(lambda x: x, str), {
            1: "1", 3: "3", 5: "5", 9: "9", 10: "10", 13: "13", 7: "7", 2: "2"})
        with self.assertRaises(TypeError):
            self.queryable_3.to_dictionary(100)
        with self.assertRaises(TypeError):
            self.queryable_3.to_dictionary(lambda x: x, 100)

    def test_to_list(self):
        self.assertEqual(self.queryable_1.to_list(), [])
        self.assertEqual(self.queryable_2.to_list(),
                         [1, 3, 5, 9, 10, 13, 7, 2])

    def test_union(self):
        self.assertEqual(list(self.queryable_1.union(self.queryable_1)), [])
        self.assertEqual(list(self.queryable_1.union(self.queryable_2)), [
            1, 3, 5, 9, 10, 13, 7, 2])
        self.assertEqual(list(self.queryable_2.union(self.queryable_2)), [
            1, 3, 5, 9, 10, 13, 7, 2])
        self.assertEqual(list(self.queryable_4.union(self.queryable_5, lambda x: x[0])), [
            [1, 2, 3], [3, 4, 5], [2, 8, 10], [4, 4, 4], [9, 5, 7], [8, 6, 2]])
        self.assertEqual(list(self.queryable_5.union(self.queryable_4, lambda x: x[0])), [
            [1, 2, 3], [4, 4, 4], [9, 5, 7], [8, 6, 2], [3, 4, 5], [2, 8, 10]])
        self.assertEqual(list(self.queryable_4.union(self.queryable_2, lambda x: x[
            0], lambda x: x)), [[1, 2, 3], [3, 4, 5], [2, 8, 10], 5, 9, 10, 13, 7])
        with self.assertRaises(TypeError):
            self.queryable_1.union(100)
        with self.assertRaises(TypeError):
            self.queryable_1.union(self.queryable_2, 100)
        with self.assertRaises(TypeError):
            self.queryable_1.union(self.queryable_2, lambda x: x, 100)

    def test_where(self):
        condition = lambda x: x > 7
        self.assertEqual(list(self.queryable_1.where(condition)), [])
        self.assertEqual(list(self.queryable_2.where(condition)), [9, 10, 13])
        with self.assertRaises(TypeError):
            self.queryable_3.where(3)
