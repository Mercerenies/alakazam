
import operator
import unittest
import alakazam as zz

class SampleError(Exception):
    pass

class TransformerTest(unittest.TestCase):

    def test_tee_1(self):
        arg = zz.of([1, 2, 3])
        (a, b) = arg.tee()
        a.consume()
        self.assertEqual(b.list(), [1, 2, 3])

    def test_tee_2(self):
        arg = zz.of([1, 2, 3])
        (a, b) = arg.tee(n = 2)
        a.consume()
        self.assertEqual(b.list(), [1, 2, 3])

    def test_id(self):
        self.assertEqual(zz.id("Alakazam"), "Alakazam")

    def test_compose_1(self):
        func = zz.compose(abs, operator.add)
        self.assertEqual(func(-1, -2), 3)

    def test_compose_2(self):
        self.assertEqual(zz.compose()("Alakazam"), "Alakazam")

    def test_raise_1(self):
        with self.assertRaises(SampleError):
            zz.raise_(SampleError("Test"))

    def test_raise_2(self):
        def foo():
            raise SampleError()
        test = 0
        with self.assertRaises(SampleError):
            try:
                foo()
            except SampleError:
                test = 1
                zz.raise_()
        self.assertEqual(test, 1)

    def test_setindex(self):
        a = [0]
        zz.setindex(a, 0, 10)
        self.assertEqual(a[0], 10)

    def test_getindex(self):
        a = [10]
        self.assertEqual(zz.getindex(a, 0), 10)

    def test_delindex(self):
        a = [10, 20, 30]
        zz.delindex(a, 1)
        self.assertEqual(a[1], 30)

    def test_not_1(self):
        self.assertTrue(zz.not_(False))

    def test_not_2(self):
        self.assertFalse(zz.not_(True))

    def test_and_1(self):
        self.assertFalse(zz.and_(False, False))

    def test_and_2(self):
        self.assertFalse(zz.and_(False, True))

    def test_and_3(self):
        self.assertTrue(zz.and_(True, True))

    def test_and_4(self):
        self.assertTrue(zz.and_())

    def test_or_1(self):
        self.assertFalse(zz.or_(False, False))

    def test_or_2(self):
        self.assertTrue(zz.or_(False, True))

    def test_or_3(self):
        self.assertTrue(zz.or_(True, True))

    def test_or_4(self):
        self.assertFalse(zz.or_())

    def test_xor_1(self):
        self.assertFalse(zz.xor())

    def test_xor_2(self):
        self.assertTrue(zz.xor(True))

    def test_xor_3(self):
        self.assertTrue(zz.xor(False, True, False))

    def test_xor_4(self):
        self.assertFalse(zz.xor(True, True, False))

    def test_xor_5(self):
        self.assertTrue(zz.xor(True, True, True))
