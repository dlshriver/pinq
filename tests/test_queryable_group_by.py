import unittest
import pinq


class queryable_group_by_tests(unittest.TestCase):

    def setUp(self):
        self.queryable = pinq.as_queryable(range(1, 11))

    def test_group_by_some_groups(self):
        self.assertEqual(list(self.queryable.group_by(lambda x: x % 2)), [
            (0, [2, 4, 6, 8, 10]), (1, [1, 3, 5, 7, 9])])

    def test_group_by_one_group(self):
        self.assertEqual(list(self.queryable.group_by(lambda x: 0)), [
            (0, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])])

    def test_group_by_individual_groups(self):
        self.assertEqual(list(self.queryable.group_by(lambda x: x)), [(1, [1]), (2, [2]), (3, [
            3]), (4, [4]), (5, [5]), (6, [6]), (7, [7]), (8, [8]), (9, [9]), (10, [10])])

    def test_group_by_some_groups_with_value_transform(self):
        self.assertEqual(list(self.queryable.group_by(lambda x: x % 2, lambda x: x * x)), [
            (0, [4, 16, 36, 64, 100]), (1, [1, 9, 25, 49, 81])])

    def test_group_by_one_group_with_value_transform(self):
        self.assertEqual(list(self.queryable.group_by(lambda x: 0, lambda x: x * x)), [
            (0, [1, 4, 9, 16, 25, 36, 49, 64, 81, 100])])

    def test_group_by_individual_groups_with_value_transform(self):
        self.assertEqual(list(self.queryable.group_by(lambda x: x, lambda x: x * x)), [
            (1, [1]), (2, [4]), (3, [9]), (4, [16]), (5, [25]), (6, [36]), (7, [49]), (
                8, [64]), (9, [81]), (10, [100])])

    def test_group_by_some_groups_with_result_transform(self):
        self.assertEqual(list(self.queryable.group_by(
            lambda x: x % 2, result_transform=lambda k, g: (k, sum(g)))), [(0, 30), (1, 25)])

    def test_group_by_one_group_with_result_transform(self):
        self.assertEqual(list(
            self.queryable.group_by(lambda x: 0, result_transform=lambda k, g: (k, sum(g)))), [
                (0, 55)])

    def test_group_by_individual_groups_with_result_transform(self):
        self.assertEqual(list(
            self.queryable.group_by(lambda x: x, result_transform=lambda k, g: (k, sum(g)))), [
                (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)])

    def test_group_by_some_groups_both_transforms(self):
        self.assertEqual(list(self.queryable.group_by(
            lambda x: x % 2, lambda x: x * x, lambda k, g: (k, sum(g)))), [(0, 220), (1, 165)])

    def test_group_by_one_group_both_transforms(self):
        self.assertEqual(list(
            self.queryable.group_by(lambda x: 0, lambda x: x * x, lambda k, g: (k, sum(g)))), [
                (0, 385)])

    def test_group_by_individual_groups_both_transforms(self):
        self.assertEqual(list(
            self.queryable.group_by(lambda x: x, lambda x: x * x, lambda k, g: (k, sum(g)))), [
                (1, 1), (2, 4), (3, 9), (4, 16), (5, 25), (6, 36),
                (7, 49), (8, 64), (9, 81), (10, 100)])

    def test_group_by_key_selector_type_error(self):
        self.assertRaises(TypeError, self.queryable.group_by, 100)

    def test_group_by_value_transform_type_error(self):
        self.assertRaises(TypeError, self.queryable.group_by,
                          lambda x: x, value_transform=100)

    def test_group_by_result_transform_type_error(self):
        self.assertRaises(TypeError, self.queryable.group_by,
                          lambda x: x, result_transform=100)
