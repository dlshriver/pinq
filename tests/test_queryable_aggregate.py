import unittest
import pinq


class queryable_aggregate_tests(unittest.TestCase):

    def setUp(self):
        self.queryable = pinq.as_queryable(range(1, 11))

    def test_aggregate_product(self):
        self.assertEqual(self.queryable.aggregate(lambda x, y: x * y), 3628800)

    def test_aggregate_product_provided_seed(self):
        self.assertEqual(self.queryable.aggregate(
            lambda x, y: x * y, seed=2), 7257600)

    def test_aggregate_product_transform_result(self):
        self.assertEqual(self.queryable.aggregate(
            lambda x, y: x * y, result_transform=lambda x: x * 2), 7257600)

    def test_aggregate_product_provided_seed_transform_result(self):
        self.assertEqual(self.queryable.aggregate(
            lambda x, y: x * y, seed=2, result_transform=lambda x: x / 2), 3628800)

    def test_aggregate_accumulator_type_error(self):
        self.assertRaises(TypeError, self.queryable.aggregate, 100)

    def test_aggregate_result_transform_type_error(self):
        self.assertRaises(TypeError, self.queryable.aggregate,
                          lambda x, y: x + y, result_transform=100)
