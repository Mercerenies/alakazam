
import unittest
import alakazam as zz

class ConversionTest(unittest.TestCase):

    def test_list(self):
        lst = ["foo", "bar", 10, 20, None]
        self.assertEqual(zz.of(lst).list(), lst)

    def test_tuple(self):
        tup = ("foo", "bar", 10, 20, None)
        self.assertEqual(zz.of(tup).tuple(), tup)

    def test_set(self):
        data = {"foo", "bar", 10, 20, None}
        self.assertEqual(zz.of(data).set(), data)

    def test_dict(self):
        data = {1: 'foo', 2: 'bar', 10: 10, "Alpha": 20, None: None}
        self.assertEqual(zz.of_dict(data).dict(), data)

