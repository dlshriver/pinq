import unittest
import pinq


class queryable_union_tests(unittest.TestCase):

    def setUp(self):
        self.queryable1 = pinq.as_queryable(range(1, 11))
        self.queryable2 = pinq.as_queryable(range(3, 8, 2))
        self.queryable3 = pinq.as_queryable(range(100, 110))

    def test_union(self):
        self.assertEqual(list(self.queryable1.union(self.queryable3)), [
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109])

    def test_union_no_additions(self):
        self.assertEqual(list(self.queryable1.union(self.queryable2)), [
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    def test_union_with_key_selector(self):
        self.assertEqual(list(self.queryable1.union(self.queryable3, lambda x: x // 8)), [
            1, 8, 100, 104])

    def test_union_no_additions_with_key_selector(self):
        self.assertEqual(list(self.queryable1.union(self.queryable2, lambda x: x // 8)), [
            1, 8])

    def test_union_other_type_error(self):
        self.assertRaises(TypeError, self.queryable1.union, 1000)

    def test_union_key_selector_type_error(self):
        self.assertRaises(TypeError, self.queryable1.union, [1, 5], 100)
