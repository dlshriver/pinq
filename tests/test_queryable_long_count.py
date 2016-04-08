import unittest
import pinq


class queryable_long_count_tests(unittest.TestCase):

    def setUp(self):
        self.queryable1 = pinq.as_queryable([])
        self.queryable2 = pinq.as_queryable(range(1))
        self.queryable3 = pinq.as_queryable(range(100))

    def test_long_count_none(self):
        self.assertEqual(self.queryable1.long_count(), 0)

    def test_long_count_one(self):
        self.assertEqual(self.queryable2.long_count(), 1)

    def test_long_count_many(self):
        self.assertEqual(self.queryable3.long_count(), 100)

    def test_long_count_with_condition_on_none(self):
        self.assertEqual(self.queryable1.long_count(lambda x: x > 12), 0)

    def test_long_count_with_condition_to_none(self):
        self.assertEqual(self.queryable2.long_count(lambda x: x > 12), 0)

    def test_long_count_with_condition_no_change(self):
        self.assertEqual(self.queryable2.long_count(lambda x: x < 12), 1)

    def test_long_count_with_condition_reduced(self):
        self.assertEqual(self.queryable3.long_count(lambda x: x < 12), 12)

    def test_long_count_condition_type_error(self):
        self.assertRaises(TypeError, self.queryable3.long_count, 100)
