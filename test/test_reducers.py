
import unittest
import functools
import alakazam as zz

@functools.total_ordering
class Contrived:
    def __init__(self, n):
        self.n = n
    def __eq__(self, other):
        return (self.n // 10) == (other.n // 10)
    def __le__(self, other):
        return (self.n // 10) <= (other.n // 10)
    def __mul__(self, other):
        return Contrived(self.n + other.n)

class ReducerTest(unittest.TestCase):

    def test_reduce_1(self):
        func = lambda x, y: y + x
        string = "CBA"
        lst = ["A", "B", "C"]
        self.assertEqual(zz.of(lst).reduce(func), string)

    def test_reduce_2(self):
        # Doesn't call the function on an empty sequence
        func = lambda x, y: zz.raise_(Exception("This should not be called"))
        self.assertEqual(zz.empty().reduce(func, init = 1), 1)

    def test_reduce_3(self):
        # Error if empty and no init
        func = lambda x, y: zz.raise_(Exception("This should not be called"))
        with self.assertRaises(zz.AlakazamError):
            zz.empty().reduce(func)

    def test_reduce_4(self):
        # Should fold from the left
        func = lambda x, y: x - y
        self.assertEqual(zz.of([1, 2, 3, 4]).reduce(func), -8)

    def test_reduce_5(self):
        # init value goes on the left
        func = lambda x, y: x - y
        self.assertEqual(zz.of([1, 2, 3, 4]).reduce(func, init = 100), 90)

    def test_foldl_1(self):
        func = lambda x, y: y + x
        string = "CBA"
        lst = ["A", "B", "C"]
        self.assertEqual(zz.of(lst).foldl(func), string)

    def test_foldl_2(self):
        # Doesn't call the function on an empty sequence
        func = lambda x, y: zz.raise_(Exception("This should not be called"))
        self.assertEqual(zz.empty().foldl(func, init = 1), 1)

    def test_foldl_3(self):
        # Error if empty and no init
        func = lambda x, y: zz.raise_(Exception("This should not be called"))
        with self.assertRaises(zz.AlakazamError):
            zz.empty().foldl(func)

    def test_foldl_4(self):
        # Should fold from the left
        func = lambda x, y: x - y
        self.assertEqual(zz.of([1, 2, 3, 4]).foldl(func), -8)

    def test_foldl_5(self):
        # init value goes on the left
        func = lambda x, y: x - y
        self.assertEqual(zz.of([1, 2, 3, 4]).foldl(func, init = 100), 90)

    def test_foldr_1(self):
        func = lambda x, y: y + x
        string = "CBA"
        lst = ["A", "B", "C"]
        self.assertEqual(zz.of(lst).foldr(func), string)

    def test_foldr_2(self):
        # Doesn't call the function on an empty sequence
        func = lambda x, y: zz.raise_(Exception("This should not be called"))
        self.assertEqual(zz.empty().foldr(func, init = 1), 1)

    def test_foldr_3(self):
        # Error if empty and no init
        func = lambda x, y: zz.raise_(Exception("This should not be called"))
        with self.assertRaises(zz.AlakazamError):
            zz.empty().foldr(func)

    def test_foldr_4(self):
        # Should fold from the right
        func = lambda x, y: x - y
        self.assertEqual(zz.of([1, 2, 3, 4]).foldr(func), -2)

    def test_foldr_5(self):
        # init value goes on the right
        func = lambda x, y: x - y
        self.assertEqual(zz.of([1, 2, 3, 4]).foldr(func, init = 100), 98)

    def test_foldr_lazy_1(self):
        func = lambda x, y: y() + x
        string = "CBA"
        lst = ["A", "B", "C"]
        self.assertEqual(zz.of(lst).foldr_lazy(func), string)

    def test_foldr_lazy_2(self):
        func = lambda x, y: zz.raise_(Exception("This should not be called"))
        self.assertEqual(zz.empty().foldr_lazy(func, init = 1), 1)

    def test_foldr_lazy_3(self):
        func = lambda x, y: zz.raise_(Exception("This should not be called"))
        with self.assertRaises(zz.AlakazamError):
            zz.empty().foldr_lazy(func)

    def test_foldr_lazy_4(self):
        func = lambda x, y: x - y()
        self.assertEqual(zz.of([1, 2, 3, 4]).foldr_lazy(func), -2)

    def test_foldr_lazy_5(self):
        func = lambda x, y: x - y()
        self.assertEqual(zz.of([1, 2, 3, 4]).foldr_lazy(func, init = 100), 98)

    def test_foldr_lazy_6(self):
        # Should stop if the argument is not called
        func = lambda x, y: x
        self.assertEqual(zz.count(999).foldr_lazy(func, init = 10), 999)

    def test_sum_1(self):
        self.assertEqual(zz.of([1, 2, 3, 4]).sum(), 10)

    def test_sum_2(self):
        # Defaults to 0
        self.assertEqual(zz.empty().sum(), 0)

    def test_sum_3(self):
        self.assertEqual(zz.of([1, 2, 3, 4]).sum(init = 500), 510)

    def test_sum_4(self):
        # Should work on any __add__ type
        self.assertEqual(zz.of(("bar", "baz")).sum(init = "foo"), "foobarbaz")

    def test_product_1(self):
        self.assertEqual(zz.of([2, 3]).product(), 6)

    def test_product_2(self):
        self.assertEqual(zz.empty().product(), 1)

    def test_product_3(self):
        self.assertEqual(zz.of([2, 2]).product(init = 4), 16)

    def test_product_4(self):
        # Should work on any __mul__ type
        self.assertEqual(zz.of((Contrived(10), Contrived(20))).product(init = Contrived(0)).n, 30)

    def test_max_1(self):
        self.assertEqual(zz.of([1, 2, 5, 3, 4]).max(), 5)

    def test_max_2(self):
        # Ignores the default if the sequence is nonempty
        self.assertEqual(zz.of([1, 2, 5, 3, 4]).max(default = 999), 5)

    def test_max_3(self):
        self.assertEqual(zz.empty().max(default = 999), 999)

    def test_max_4(self):
        self.assertEqual(zz.of([5, 1, 2, 3, 4]).max(key = lambda x: - x), 1)

    def test_max_5(self):
        # Always gets the first match if equal
        self.assertEqual(zz.of([Contrived(14), Contrived(15), Contrived(9)]).max().n, 14)

    def test_max_6(self):
        with self.assertRaises(zz.AlakazamError):
            zz.empty().max()

    def test_min_1(self):
        self.assertEqual(zz.of([5, 2, 1, 3, 4]).min(), 1)

    def test_min_2(self):
        # Ignores the default if the sequence is nonempty
        self.assertEqual(zz.of([5, 2, 1, 3, 4]).min(default = -999), 1)

    def test_min_3(self):
        self.assertEqual(zz.empty().min(default = 999), 999)

    def test_min_4(self):
        self.assertEqual(zz.of([2, 5, 1, 3, 4]).min(key = lambda x: - x), 5)

    def test_min_5(self):
        # Always gets the first match if equal
        self.assertEqual(zz.of([Contrived(15), Contrived(14), Contrived(22)]).min().n, 15)

    def test_min_6(self):
        with self.assertRaises(zz.AlakazamError):
            zz.empty().min()

    def test_find_1(self):
        self.assertEqual(zz.range(10).find(lambda x: x > 5), 6)

    def test_find_2(self):
        self.assertEqual(zz.range(10).find(lambda x: False), None)

    def test_find_3(self):
        self.assertEqual(zz.range(10).find(lambda x: False, default = "No"), "No")

    def test_all_1(self):
        self.assertTrue(zz.range(10, 20, 2).all(lambda x: x % 2 == 0))

    def test_all_2(self):
        self.assertFalse(zz.range(10, 20).all(lambda x: x < 19))

    def test_all_3(self):
        self.assertTrue(zz.of([True, True, True]).all())

    def test_all_4(self):
        self.assertTrue(zz.empty().all())

    def test_all_5(self):
        # Short-circuits on infinite sequences
        self.assertFalse(zz.repeat(False).all())

    def test_any_1(self):
        self.assertEqual(zz.range(-10, 10).any(lambda x: max(x, 0)), 1)

    def test_any_2(self):
        self.assertEqual(zz.range(10, 20).any(lambda x: x > 50), False)

    def test_any_3(self):
        self.assertEqual(zz.of([False, True, False]).any(), True)

    def test_any_4(self):
        self.assertEqual(zz.of([False, None, False]).any(), False)

    def test_any_5(self):
        self.assertEqual(zz.of([False, None, False]).any(default = -1), -1)

    def test_any_6(self):
        self.assertEqual(zz.empty().any(default = -1), -1)

    def test_any_7(self):
        # Short-circuits on infinite sequences
        self.assertTrue(zz.count(1).any(lambda x: x > 100))

    def test_null_1(self):
        self.assertTrue(zz.empty().null())

    def test_null_2(self):
        self.assertFalse(zz.of((1,)).null())

    def test_null_3(self):
        # Works on infinite lists
        self.assertFalse(zz.count(1).null())

    def test_length_1(self):
        self.assertEqual(zz.empty().length(), 0)

    def test_length_2(self):
        self.assertEqual(zz.range(10, 20, 2).length(), 5)

    def test_length_3(self):
        self.assertEqual(zz.count(1).take(50).length(), 50)

    def test_consume_1(self):
        self.assertEqual(zz.of([1, 2, 3]).consume(), None)

    def test_consume_2(self):
        x = {1: -10}
        def foo(y):
            x[1] = y
            return y
        zz.of([1, 2, 3]).map(foo).consume()
        self.assertEqual(x[1], 3)

    def test_consume_3(self):
        x = {1: -10}
        def foo(y):
            x[1] = y
            return y
        zz.of([1, 2, 3]).map(foo) # Don't consume
        self.assertEqual(x[1], -10)

    def test_consume_4(self):
        x = {1: -10}
        def foo(y):
            x[1] = y
            return True
        zz.of([1, 2, 3]).filter(foo) # Don't consume
        self.assertEqual(x[1], -10)

    def test_consume_5(self):
        x = {1: -10}
        def foo(y):
            x[1] = y
            return True
        zz.of([1, 2, 3]).filterfalse(foo) # Don't consume
        self.assertEqual(x[1], -10)

    def test_string_1(self):
        self.assertEqual(zz.of(['abc', 'def', 'ghi']).string(), 'abcdefghi')

    def test_string_2(self):
        with self.assertRaises(zz.AlakazamError):
            zz.of(['abc', 3, 'ghi']).string()
