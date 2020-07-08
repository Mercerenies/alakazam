
import unittest
import alakazam as zz
from alakazam import _1, _2, _3, _4, _5

class UnaryOpMock(object):

    def __init__(self, txt):
        self.txt = txt

    def __str__(self):
        return self.txt

    def __repr__(self):
        return self.txt

    def __eq__(self, other):
        return type(self) == type(other) and self.txt == other.txt

    def __hash__(self):
        return hash((type(self), self.txt))

    def __neg__(self):
        return UnaryOpMock("-" + self.txt)

    def __pos__(self):
        return UnaryOpMock("+" + self.txt)

    def __invert__(self):
        return UnaryOpMock("~" + self.txt)

class SimpleClass(object):

    def __init__(self, n, m):
        self.n = n
        self.m = m

    def sum(self):
        return self.n + self.m

def all_args(*args, **kwargs):
    return (args, kwargs)

class AnonymousTest(unittest.TestCase):

    def test_add_1(self):
        fn = _1 + _2
        self.assertEqual(fn(10, 20), 30)
        self.assertEqual(fn(10, 10), 20)

    def test_add_2(self):
        fn = _1 + _1
        self.assertEqual(fn(10), 20)

    def test_add_3(self):
        fn = _1 + 10
        self.assertEqual(fn(90), 100)

    def test_add_4(self):
        fn = 10 + _1
        self.assertEqual(fn(90), 100)

    def test_add_5(self):
        fn = "foo" + _1
        self.assertEqual(fn("bar"), "foobar")

    def test_sub_1(self):
        fn = _1 - _2
        self.assertEqual(fn(20, 15), 5)

    def test_sub_2(self):
        fn = _1 - _3
        self.assertEqual(fn(20, 999, 5), 15)

    def test_sub_3(self):
        fn = _1 - 1
        self.assertEqual(fn(20), 19)

    def test_sub_4(self):
        fn = 1 - _1
        self.assertEqual(fn(10), -9)

    def test_mul_1(self):
        fn = _1 * _2
        self.assertEqual(fn(10, 20), 200)
        self.assertEqual(fn(20, 10), 200)

    def test_mul_2(self):
        fn = _1 * 3
        self.assertEqual(fn(10), 30)
        self.assertEqual(fn("foo"), "foofoofoo")
        self.assertEqual(fn([1]), [1, 1, 1])

    def test_mul_3(self):
        fn = 3 * _1
        self.assertEqual(fn(10), 30)
        self.assertEqual(fn("foo"), "foofoofoo")
        self.assertEqual(fn([1]), [1, 1, 1])

    def test_div_1(self):
        fn = _1 / 2
        self.assertEqual(fn(10), 5)
        self.assertEqual(fn(5), 2.5)

    def test_div_2(self):
        fn = _2 / _1
        self.assertEqual(fn(2, 10), 5)

    def test_div_3(self):
        fn = 10 / _1
        self.assertEqual(fn(5), 2)
        with self.assertRaises(ZeroDivisionError):
            fn(0)

    def test_floordiv_1(self):
        fn = _1 // 2
        self.assertEqual(fn(10), 5)
        self.assertEqual(fn(5), 2)

    def test_floordiv_2(self):
        fn = _2 // _1
        self.assertEqual(fn(3, 10), 3)

    def test_floordiv_3(self):
        fn = 10 // _1
        self.assertEqual(fn(6), 1)
        with self.assertRaises(ZeroDivisionError):
            fn(0)

    def test_mod_1(self):
        fn = _1 % 10
        self.assertEqual(fn(4), 4)
        self.assertEqual(fn(16), 6)
        self.assertEqual(fn(0), 0)
        self.assertEqual(fn(".%s."), ".10.")

    def test_mod_2(self):
        fn = _1 % _2
        self.assertEqual(fn(4, 3), 1)

    def test_mod_3(self):
        fn = 10 % _1
        self.assertEqual(fn(8), 2)
        self.assertEqual(fn(11), 10)
        with self.assertRaises(ZeroDivisionError):
            fn(0)

    def test_pow_1(self):
        fn = _1 ** 2
        self.assertEqual(fn(3), 9)
        self.assertEqual(fn(2), 4)

    def test_pow_2(self):
        fn = 2 ** _1
        self.assertEqual(fn(0), 1)
        self.assertEqual(fn(3), 8)

    def test_pow_3(self):
        fn = _1 ** _2
        self.assertEqual(fn(2, 5), 32)
        self.assertEqual(fn(3, 3), 27)

    def test_lshift_1(self):
        fn = _1 << 2
        self.assertEqual(fn(3), 12)
        self.assertEqual(fn(0), 0)

    def test_lshift_2(self):
        fn = 3 << _1
        self.assertEqual(fn(0), 3)
        self.assertEqual(fn(1), 6)
        self.assertEqual(fn(2), 12)

    def test_lshift_3(self):
        fn = _1 << _2
        self.assertEqual(fn(2, 2), 8)

    def test_rshift_1(self):
        fn = _1 >> 1
        self.assertEqual(fn(10), 5)
        self.assertEqual(fn(9), 4)

    def test_rshift_2(self):
        fn = 3 >> _1
        self.assertEqual(fn(0), 3)
        self.assertEqual(fn(1), 1)
        self.assertEqual(fn(2), 0)

    def test_rshift_3(self):
        fn = _1 >> _2
        self.assertEqual(fn(5, 1), 2)

    def test_and_1(self):
        fn = _1 & 3
        self.assertEqual(fn(3), 3)
        self.assertEqual(fn(5), 1)
        self.assertEqual(fn(6), 2)

    def test_and_2(self):
        fn = 3 & _1
        self.assertEqual(fn(3), 3)
        self.assertEqual(fn(5), 1)
        self.assertEqual(fn(6), 2)

    def test_and_3(self):
        fn = _1 & _2
        self.assertEqual(fn(3, 3), 3)
        self.assertEqual(fn(5, 3), 1)
        self.assertEqual(fn(3, 6), 2)

    def test_or_1(self):
        fn = _1 | 3
        self.assertEqual(fn(3), 3)
        self.assertEqual(fn(5), 7)
        self.assertEqual(fn(6), 7)

    def test_or_2(self):
        fn = 3 | _1
        self.assertEqual(fn(3), 3)
        self.assertEqual(fn(5), 7)
        self.assertEqual(fn(6), 7)

    def test_or_3(self):
        fn = _1 | _2
        self.assertEqual(fn(3, 3), 3)
        self.assertEqual(fn(5, 3), 7)
        self.assertEqual(fn(3, 6), 7)

    def test_xor_1(self):
        fn = _1 ^ 3
        self.assertEqual(fn(3), 0)
        self.assertEqual(fn(5), 6)
        self.assertEqual(fn(6), 5)

    def test_xor_2(self):
        fn = 3 ^ _1
        self.assertEqual(fn(3), 0)
        self.assertEqual(fn(5), 6)
        self.assertEqual(fn(6), 5)

    def test_xor_3(self):
        fn = _1 ^ _2
        self.assertEqual(fn(3, 3), 0)
        self.assertEqual(fn(5, 3), 6)
        self.assertEqual(fn(3, 6), 5)

    def test_pos(self):
        fn = + _1
        self.assertEqual(fn(10), 10)
        self.assertEqual(fn(UnaryOpMock("abc")), UnaryOpMock("+abc"))

    def test_neg(self):
        fn = - _1
        self.assertEqual(fn(5), -5)
        self.assertEqual(fn(UnaryOpMock("abc")), UnaryOpMock("-abc"))

    def test_invert(self):
        fn = ~ _1
        self.assertEqual(fn(0), -1)
        self.assertEqual(fn(UnaryOpMock("abc")), UnaryOpMock("~abc"))

    def test_eq(self):
        self.assertEqual((_1 == 0)(-1), False)
        self.assertEqual((_1 == 0)( 0), True )
        self.assertEqual((_1 == 0)(+1), False)

        self.assertEqual((0 == _1)(-1), False)
        self.assertEqual((0 == _1)( 0), True )
        self.assertEqual((0 == _1)(+1), False)

        self.assertEqual((_1 == _2)(0, -1), False)
        self.assertEqual((_1 == _2)(0,  0), True )
        self.assertEqual((_1 == _2)(0, +1), False)

    def test_ne(self):
        self.assertEqual((_1 != 0)(-1), True )
        self.assertEqual((_1 != 0)( 0), False)
        self.assertEqual((_1 != 0)(+1), True )

        self.assertEqual((0 != _1)(-1), True )
        self.assertEqual((0 != _1)( 0), False)
        self.assertEqual((0 != _1)(+1), True )

        self.assertEqual((_1 != _2)(0, -1), True )
        self.assertEqual((_1 != _2)(0,  0), False)
        self.assertEqual((_1 != _2)(0, +1), True )

    def test_lt(self):
        self.assertEqual((_1 < 0)(-1), True )
        self.assertEqual((_1 < 0)( 0), False)
        self.assertEqual((_1 < 0)(+1), False)

        self.assertEqual((0 < _1)(-1), False)
        self.assertEqual((0 < _1)( 0), False)
        self.assertEqual((0 < _1)(+1), True )

        self.assertEqual((_1 < _2)(0, -1), False)
        self.assertEqual((_1 < _2)(0,  0), False)
        self.assertEqual((_1 < _2)(0, +1), True )

    def test_le(self):
        self.assertEqual((_1 <= 0)(-1), True )
        self.assertEqual((_1 <= 0)( 0), True )
        self.assertEqual((_1 <= 0)(+1), False)

        self.assertEqual((0 <= _1)(-1), False)
        self.assertEqual((0 <= _1)( 0), True )
        self.assertEqual((0 <= _1)(+1), True )

        self.assertEqual((_1 <= _2)(0, -1), False)
        self.assertEqual((_1 <= _2)(0,  0), True )
        self.assertEqual((_1 <= _2)(0, +1), True )

    def test_gt(self):
        self.assertEqual((_1 > 0)(-1), False)
        self.assertEqual((_1 > 0)( 0), False)
        self.assertEqual((_1 > 0)(+1), True )

        self.assertEqual((0 > _1)(-1), True )
        self.assertEqual((0 > _1)( 0), False)
        self.assertEqual((0 > _1)(+1), False)

        self.assertEqual((_1 > _2)(0, -1), True )
        self.assertEqual((_1 > _2)(0,  0), False)
        self.assertEqual((_1 > _2)(0, +1), False)

    def test_ge(self):
        self.assertEqual((_1 >= 0)(-1), False)
        self.assertEqual((_1 >= 0)( 0), True )
        self.assertEqual((_1 >= 0)(+1), True )

        self.assertEqual((0 >= _1)(-1), True )
        self.assertEqual((0 >= _1)( 0), True )
        self.assertEqual((0 >= _1)(+1), False)

        self.assertEqual((_1 >= _2)(0, -1), True )
        self.assertEqual((_1 >= _2)(0,  0), True )
        self.assertEqual((_1 >= _2)(0, +1), False)

    def test_getattr_1(self):
        obj = SimpleClass(10, 20)
        self.assertEqual((_1.n)(obj), 10)
        self.assertEqual((_1.m)(obj), 20)

    def test_getattr_2(self):
        obj = SimpleClass(10, 20)
        self.assertEqual((_1.sum)(obj)(), 30)

    def test_getitem_1(self):
        obj = ["foo", "bar", "baz"]
        self.assertEqual((_1[0])(obj), "foo")
        self.assertEqual((_1[1])(obj), "bar")
        self.assertEqual((_1[2])(obj), "baz")
        with self.assertRaises(IndexError):
            (_1[3])(obj)

    def test_getitem_2(self):
        obj = {"foo": 100, "bar": 200, "baz": 300}
        self.assertEqual((_1["foo"])(obj), 100)
        self.assertEqual((_1["bar"])(obj), 200)
        self.assertEqual((_1["baz"])(obj), 300)
        with self.assertRaises(KeyError):
            (_1["frobnicate"])(obj)

    def test_getitem_3(self):
        obj = ["foo", "bar", "baz"]
        fn = _1[_2]
        self.assertEqual(fn(obj, 0), "foo")
        self.assertEqual(fn(obj, 1), "bar")
        self.assertEqual(fn(obj, 2), "baz")
        with self.assertRaises(IndexError):
            fn(obj, 3)

    def test_arg(self):
        fn = zz.arg(5) + zz.arg(6)
        arglist = [10, 20, 30, 40, 50, 60]
        self.assertEqual(fn(*arglist), 110)

    def test_kwarg(self):
        fn = zz.kwarg("a") - zz.kwarg("b")
        self.assertEqual(fn("unrelated position argument", a=5, b=6, c=100), -1)

    def test_var_1(self):
        fn = zz.var(200)
        # Doesn't matter what arguments I pass
        self.assertEqual(fn(), 200)
        self.assertEqual(fn(0, 100), 200)
        self.assertEqual(fn(None, "foobar", default=object(), key=lambda x: x), 200)
        self.assertEqual(fn(200, object, var={'a': 1}, py="Python"), 200)

    def test_var_2(self):
        # Equivalent to just _1 + 100, but we're explicitly wrapping
        # the number.
        fn = _1 + zz.var(100)
        self.assertEqual(fn(10), 110)
        self.assertEqual(fn(-1), 99)
        self.assertEqual(fn(0), 100)

    def test_var_3(self):
        obj = ["foo", "bar", "baz"]
        fn = zz.var(obj)[_1]
        self.assertEqual(fn(0), "foo")
        self.assertEqual(fn(1), "bar")
        self.assertEqual(fn(2), "baz")
        with self.assertRaises(IndexError):
            fn(3)

    def test_var_4(self):
        # Currying. Please don't do this in production code.
        fn = _1 - zz.var(_1)
        self.assertEqual(fn(10)(5), 5)
        self.assertEqual(fn(10)(3), 7)
        self.assertEqual(fn(5)(6), -1)

    def test_bind_1(self):
        fn = zz.bind(all_args)(100, 200, a=1)
        self.assertEqual(fn(), ((100, 200), {'a': 1}))
        self.assertEqual(fn(-1, a=2, b=3), ((100, 200), {'a': 1}))

    def test_bind_2(self):
        fn = zz.bind(all_args)(_2, _1)
        self.assertEqual(fn(100, 200), ((200, 100), {}))
        self.assertEqual(fn("foo", "bar", a=-1), (("bar", "foo"), {}))

    def test_bind_3(self):
        fn = zz.bind(all_args)(1000, _1)
        self.assertEqual(fn(10), ((1000, 10), {}))

    def test_bind_4(self):
        fn = zz.bind(all_args)(_1, "foo", a=_2)
        self.assertEqual(fn(-1, None), ((-1, "foo"), {'a': None}))

    def test_bind_5(self):
        fn = zz.bind(all_args)(zz.kwarg('foo'), "bar", a=zz.kwarg('foo'))
        self.assertEqual(fn(foo=1000), ((1000, "bar"), {'a': 1000}))

    def test_bind_6(self):
        fn = zz.bind(all_args)()
        self.assertEqual(fn(10, 20, None, foo="bar", a=3), ((), {}))

    def test_bind_7(self):
        fn = zz.bind(all_args, 100, 200, a=1)
        self.assertEqual(fn(), ((100, 200), {'a': 1}))
        self.assertEqual(fn(-1, a=2, b=3), ((100, 200), {'a': 1}))

    def test_bind_8(self):
        fn = zz.bind(all_args, _2, _1)
        self.assertEqual(fn(100, 200), ((200, 100), {}))
        self.assertEqual(fn("foo", "bar", a=-1), (("bar", "foo"), {}))

    def test_bind_9(self):
        fn = zz.bind(all_args, 1000, _1)
        self.assertEqual(fn(10), ((1000, 10), {}))

    def test_bind_10(self):
        fn = zz.bind(all_args, _1, "foo", a=_2)
        self.assertEqual(fn(-1, None), ((-1, "foo"), {'a': None}))

    def test_bind_11(self):
        fn = zz.bind(all_args, zz.kwarg('foo'), "bar", a=zz.kwarg('foo'))
        self.assertEqual(fn(foo=1000), ((1000, "bar"), {'a': 1000}))
