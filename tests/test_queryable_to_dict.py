import unittest
import pinq


class queryable_to_dict_tests(unittest.TestCase):

    def setUp(self):
        self.queryable = pinq.as_queryable(range(1, 6))

    def test_to_dict(self):
        self.assertEqual(self.queryable.to_dict(
            lambda x: x - 1), {0: 1, 1: 2, 2: 3, 3: 4, 4: 5})

    def test_to_dict_with_value_selector(self):
        self.assertEqual(self.queryable.to_dict(
            lambda x: x - 1, lambda x: chr(x + 64)), {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E'})

    def test_to_dict_key_selector_type_error(self):
        self.assertRaises(TypeError, self.queryable.to_dict, 219853)

    def test_to_dict_value_selector_type_error(self):
        self.assertRaises(
            TypeError, self.queryable.to_dict, lambda x: x, 219853)
