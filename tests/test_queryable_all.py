import unittest
import pinq


class queryable_all_tests(unittest.TestCase):

    def setUp(self):
        self.queryable = pinq.as_queryable(range(1, 11))

    def test_all_return_true(self):
        self.assertEqual(self.queryable.all(lambda x: x > 0), True)

    def test_all_return_false(self):
        self.assertEqual(self.queryable.all(lambda x: x < 10), False)

    def test_all_predicate_type_error(self):
        self.assertRaises(TypeError, self.queryable.all, 100)
