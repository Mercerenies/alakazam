
import unittest
import functools
import alakazam as zz

from test_util import SampleError

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

    def test_foldr_6(self):
        # Works even after chained with other iterators
        func = lambda x, y: x + y
        self.assertEqual(zz.of([1, 2, 3, 4]).map(lambda x: x + 1).foldr(func, init = 100), 114)

    def test_foldr_7(self):
        # Type errors during iteration get passed through
        func = lambda x, y: zz.raise_(TypeError("This exception should be raised"))
        with self.assertRaises(TypeError):
            zz.of([1, 2, 3, 4]).foldr(func)

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

    def test_absorb_1(self):
        res = zz.range(5).absorb(lambda x, y: x.append(y), [])
        self.assertEqual(res, list(range(5)))

    def test_absorb_2(self):
        def f(x, y):
            x[y] = 2
        res = zz.of(["a", "b", "c"]).absorb(f, {})
        self.assertEqual(res, {"a": 2, "b": 2, "c": 2})

    def test_absorb_3(self):
        obj = object()
        res = zz.range(10).absorb(lambda x, y: 0, obj)
        self.assertEqual(obj, res)

    def test_absorb_4(self):
        test = [0]
        def f(x, y):
            test[0] += 1
        zz.range(10).absorb(f, None)
        self.assertEqual(test, [10])

    def test_absorb_5(self):
        def f(x, y):
            return 99
        self.assertEqual(zz.of([1, 2, 3]).absorb(f, "foobar"), "foobar")

    def test_absorb_6(self):
        def f(x, y):
            raise SampleError("Error function")
        with self.assertRaises(SampleError):
            zz.of([None]).absorb(f, {})

    def test_absorb_7(self):
        def f(x, y):
            raise Exception("This exception should never be raised")
        self.assertEqual(zz.empty().absorb(f, "lorem ipsum"), "lorem ipsum")

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

    def test_string_3(self):
        self.assertEqual(zz.empty().string(), '')

    def test_join_1(self):
        self.assertEqual(zz.of(['abc', 'def', 'ghi']).join(), 'abc,def,ghi')

    def test_join_2(self):
        with self.assertRaises(zz.AlakazamError):
            zz.of(['abc', 3, 'ghi']).join()

    def test_join_3(self):
        with self.assertRaises(zz.AlakazamError):
            zz.of(['abc', 3, 'ghi']).join('**')

    def test_join_4(self):
        self.assertEqual(zz.of(['abc', 'def', 'ghi']).join('**'), 'abc**def**ghi')

    def test_join_5(self):
        self.assertEqual(zz.of(['abc', 'def', 'ghi']).join(''), 'abcdefghi')

    def test_apply_1(self):
        self.assertEqual(zz.range(5).apply(list), list(range(5)))

    def test_apply_2(self):
        gen = zz.count(0) # Infinite sequence
        self.assertEqual(gen.apply(lambda _: "example text"), "example text")

    def test_apply_3(self):
        gen = zz.range(5)
        self.assertEqual(zz.range(5).apply(sum), 10)

    def test_apply_4(self):
        def f(x):
            x = list(x)
            return x[0] + x[2]
        self.assertEqual(zz.of([10, -20, 30]).apply(f), 40)

    def test_apply_5(self):
        ex = { 'foo': 0 }
        def f(x):
            # nonlocal ex (can't do this, for Python 2 compatibility)
            ex['foo'] += 1
        # Any call to apply calls the function exactly once
        zz.range(10).apply(f)
        zz.of([1, 2, 3]).apply(f)
        zz.empty().apply(f)
        self.assertEqual(ex['foo'], 3)

    def test_apply_6(self):
        def f(x):
            raise SampleError("This function raises an error")
        with self.assertRaises(SampleError):
            zz.empty().apply(f)

    def test_each_1(self):
        def f(x):
            raise SampleError("This error should not be raised")
        zz.empty().each(f)

    def test_each_2(self):
        def f(x):
            raise SampleError("This error should not be raised")
        with self.assertRaises(SampleError):
            zz.repeat(0).each(f)

    def test_each_3(self):
        # Singleton list to work around lack of nonlocal support in Python 2
        n = [0]
        def f(x):
            n[0] += 1
        zz.of([10, 20, 30, 40]).each(f)
        self.assertEqual(n[0], 4)

    def test_each_4(self):
        # Singleton list to work around lack of nonlocal support in Python 2
        n = [0]
        def f(x):
            n[0] += x
        zz.of([10, 20, 30, 40]).each(f)
        self.assertEqual(n[0], 100)

    def test_first_1(self):
        arg = zz.of([1, 2, 3, 4])
        self.assertEqual(arg.first(), 1)

    def test_first_2(self):
        arg = zz.of([1, 2, 3, 4])
        self.assertEqual(arg.first(default = "foobar"), 1)

    def test_first_3(self):
        arg = zz.of([])
        self.assertEqual(arg.first(default = "foobar"), "foobar")

    def test_first_4(self):
        arg = zz.of([])
        with self.assertRaises(zz.AlakazamError):
            arg.first()

    def test_index_1(self):
        pos = zz.of(["foo", "bar", "baz", "bar"]).index(lambda x: x == "bar")
        self.assertEqual(pos, 1)

    def test_index_2(self):
        pos = zz.of(["foo", "bar", "baz", "bar"]).index(lambda x: True)
        self.assertEqual(pos, 0)

    def test_index_3(self):
        pos = zz.of(["foo", "bar", "baz", "bar"]).index(lambda x: False)
        self.assertEqual(pos, None)

    def test_index_4(self):
        tmp = object()
        pos = zz.of(["foo", "bar", "baz", "bar"]).index(lambda x: False, default = tmp)
        self.assertEqual(pos, tmp)

    def test_index_5(self):
        tmp = object()
        pos = zz.of(["foo", "bar", "baz", "bar"]).index(lambda x: x == "bar", default = tmp)
        self.assertEqual(pos, 1)

    def test_index_6(self):
        pos = zz.count(0, step=1).index(lambda x: x % 3 == 1)
        self.assertEqual(pos, 1)

    def test_index_7(self):
        pos = zz.count(0, step=1).drop(2).index(lambda x: x % 3 == 1)
        self.assertEqual(pos, 2)

    def test_index_8(self):
        # Providing no function
        pos = zz.of([0, 1, True, False]).index()
        self.assertEqual(pos, 1)
