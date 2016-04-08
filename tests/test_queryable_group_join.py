import unittest
import pinq


class queryable_group_join_tests(unittest.TestCase):

    def setUp(self):
        self.queryable0 = pinq.as_queryable([])
        self.queryable1 = pinq.as_queryable(range(2))
        self.queryable2 = pinq.as_queryable(range(10))

    def test_group_join_all_match_two_arg_result_transform(self):
        self.assertEqual(list(self.queryable1.group_join(
            self.queryable2, lambda x: x, lambda x: x % 2, lambda x, y: y)), [
                [0, 2, 4, 6, 8], [1, 3, 5, 7, 9]])

    def test_group_join_all_match(self):
        self.assertEqual(list(self.queryable1.group_join(
            self.queryable2, lambda x: x, lambda x: x % 2, lambda x: x)), [
                (0, [0, 2, 4, 6, 8]), (1, [1, 3, 5, 7, 9])])

    def test_group_join_some_match(self):
        self.assertEqual(list(self.queryable1.group_join(
            self.queryable2, lambda x: x, lambda x: x // 2, lambda x: x)), [
                (0, [0, 1]), (1, [2, 3])])

    def test_group_join_none_match(self):
        self.assertEqual(list(self.queryable1.group_join(
            self.queryable2, lambda x: x, lambda x: x + 100, lambda x: x)), [
                (0, []), (1, [])])

    def test_group_join_some_no_match(self):
        self.assertEqual(list(self.queryable2.group_join(
            self.queryable1, lambda x: x, lambda x: x * 3, lambda x: x)), [
                (0, [0]), (1, []), (2, []), (3, [1]), (4, []), (5, []),
                (6, []), (7, []), (8, []), (9, [])])

    def test_group_join_inner_to_multiple_outer(self):
        self.assertEqual(list(self.queryable1.group_join(
            self.queryable2, lambda x: 0, lambda x: x % 2, lambda x: x)), [
                (0, [0, 2, 4, 6, 8]), (1, [0, 2, 4, 6, 8])])

    def test_group_join_empty_outer(self):
        self.assertEqual(list(self.queryable0.group_join(
            self.queryable2, lambda x: x, lambda x: x % 2, lambda x: x)), [])

    def test_group_join_empty_inner(self):
        self.assertEqual(list(self.queryable1.group_join(
            self.queryable0, lambda x: x, lambda x: x % 2, lambda x: x)), [
                (0, []), (1, [])])

    def test_group_join_other_type_error(self):
        self.assertRaises(TypeError, self.queryable1.group_join,
                          100, lambda x: x, lambda x: x, lambda x: x)

    def test_group_join_key_selector_type_error(self):
        self.assertRaises(TypeError, self.queryable1.group_join,
                          self.queryable1, "apple", lambda x: x, lambda x: x)

    def test_group_join_other_key_selector_type_error(self):
        self.assertRaises(TypeError, self.queryable1.group_join,
                          self.queryable1, lambda x: x, 100016, lambda x: x)

    def test_group_join_result_transform_type_error(self):
        self.assertRaises(TypeError, self.queryable1.group_join,
                          self.queryable1, lambda x: x, lambda x: x, [])
