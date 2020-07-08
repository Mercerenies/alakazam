
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

    def test_sorted_1(self):
        self.assertEqual(zz.of([3, 1, 2, 0]).sorted(), [0, 1, 2, 3])

    def test_sorted_2(self):
        self.assertEqual(zz.of([3, 1, 2, 0]).sorted(reverse=True), [3, 2, 1, 0])

    def test_sorted_3(self):
        self.assertEqual(zz.of([10, 9, 11]).sorted(), [9, 10, 11])

    def test_sorted_4(self):
        # Lexicographic ordering
        self.assertEqual(zz.of([10, 9, 11]).sorted(key=str), [10, 11, 9])

    def test_sorted_5(self):
        # Lexicographic ordering (reversed)
        self.assertEqual(zz.of([10, 9, 11]).sorted(key=str, reverse=True), [9, 11, 10])
