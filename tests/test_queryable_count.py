import unittest
import pinq


class queryable_count_tests(unittest.TestCase):

    def setUp(self):
        self.queryable1 = pinq.as_queryable([])
        self.queryable2 = pinq.as_queryable(range(1))
        self.queryable3 = pinq.as_queryable(range(100))

    def test_count_none(self):
        self.assertEqual(self.queryable1.count(), 0)

    def test_count_one(self):
        self.assertEqual(self.queryable2.count(), 1)

    def test_count_many(self):
        self.assertEqual(self.queryable3.count(), 100)

    def test_count_with_condition_on_none(self):
        self.assertEqual(self.queryable1.count(lambda x: x > 12), 0)

    def test_count_with_condition_to_none(self):
        self.assertEqual(self.queryable2.count(lambda x: x > 12), 0)

    def test_count_with_condition_no_change(self):
        self.assertEqual(self.queryable2.count(lambda x: x < 12), 1)

    def test_count_with_condition_reduced(self):
        self.assertEqual(self.queryable3.count(lambda x: x < 12), 12)

    def test_count_condition_type_error(self):
        self.assertRaises(TypeError, self.queryable3.count, 100)
