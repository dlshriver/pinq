import unittest
import pinq


class queryable_any_tests(unittest.TestCase):

    def setUp(self):
        self.queryable = pinq.as_queryable(range(1, 11))

    def test_any_return_true(self):
        self.assertEqual(self.queryable.any(lambda x: x > 6), True)

    def test_any_return_false(self):
        self.assertEqual(self.queryable.any(lambda x: x > 10), False)

    def test_any_predicate_type_error(self):
        self.assertRaises(TypeError, self.queryable.any, 100)
