
import unittest
import alakazam as zz
from alakazam import _1, _2, _3, _4, _5

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


    # /////
