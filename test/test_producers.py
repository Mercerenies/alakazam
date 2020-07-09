
import unittest
import alakazam as zz

class ProducerTest(unittest.TestCase):

    def test_of(self):
        iterable = zz.of([1, 2, 3, 4, 5])
        self.assertEqual(iterable.list(), [1, 2, 3, 4, 5])

    def test_of_dict(self):
        iterable = zz.of_dict({'a': 1, 'b': 2})
        result = iterable.set()
        keys = set([('a', 1), ('b', 2)])
        self.assertEqual(result, keys)

    def test_range_1(self):
        value1 = zz.range(10).list()
        value2 = list(range(10))
        self.assertEqual(value1, value2)

    def test_range_2(self):
        value1 = zz.range(5, 15).list()
        value2 = list(range(5, 15))
        self.assertEqual(value1, value2)

    def test_range_3(self):
        value1 = zz.range(5, 20, 2).list()
        value2 = list(range(5, 20, 2))
        self.assertEqual(value1, value2)

    def test_range_4(self):
        value1 = zz.range(20, 5, -1).list()
        value2 = list(range(20, 5, -1))
        self.assertEqual(value1, value2)

    def test_empty(self):
        self.assertEqual(list(zz.empty()), [])

    def test_iterate_1(self):
        iterable = zz.iterate(lambda x: x + 2, 1)
        self.assertEqual(iterable.take(5).list(), [1, 3, 5, 7, 9])

    def test_iterate_2(self):
        iterable = zz.iterate(lambda x: "foo", 0)
        self.assertEqual(iterable.take(3).list(), [0, "foo", "foo"])

    def test_zipup_1(self):
        iterable = zz.zipup([1, 2], ["A", "B"])
        self.assertEqual(iterable.list(), [(1, "A"), (2, "B")])

    def test_zipup_2(self):
        # Make sure it truncates on the right
        iterable = zz.zipup(["foo", "bar"], zz.repeat(1))
        self.assertEqual(iterable.list(), [("foo", 1), ("bar", 1)])

    def test_zipup_3(self):
        # Make sure it truncates on the left
        iterable = zz.zipup(zz.repeat(1), ["foo", "bar"])
        self.assertEqual(iterable.list(), [(1, "foo"), (1, "bar")])

    def test_zipup_4(self):
        # Make sure it works given no arguments
        iterable = zz.zipup()
        self.assertEqual(iterable.list(), [])

    def test_zipup_5(self):
        # Make sure it works in the infinite case
        iterable = zz.zipup(zz.repeat(1), zz.repeat(2))
        self.assertEqual(iterable.take(2).list(), [(1, 2), (1, 2)])

    def test_count_1(self):
        iterable = zz.count(10).take(10)
        result = range(10, 20)
        self.assertEqual(list(iterable), list(result))

    def test_count_2(self):
        iterable = zz.count(10, 2).take(10)
        result = range(10, 30, 2)
        self.assertEqual(list(iterable), list(result))

    def test_repeat_1(self):
        iterable = zz.repeat(12).take(2)
        self.assertEqual(list(iterable), [12, 12])

    def test_repeat_2(self):
        iterable = zz.repeat(12, n = 2)
        self.assertEqual(list(iterable), [12, 12])

    def test_chainup_1(self):
        self.assertEqual(zz.chainup([1, 2, 3], [4, 5, 6]).list(), [1, 2, 3, 4, 5, 6])

    def test_chainup_2(self):
        self.assertEqual(zz.chainup([1, 2, 3], [], [4], [5], (6,)).list(), [1, 2, 3, 4, 5, 6])

    def test_chainup_3(self):
        self.assertEqual(zz.chainup(()).list(), [])

    def test_chainup_4(self):
        self.assertEqual(zz.chainup().list(), [])

    def test_chainup_lazy_1(self):
        self.assertEqual(zz.chainup_lazy([[1, 2, 3], [4, 5, 6]]).list(), [1, 2, 3, 4, 5, 6])

    def test_chainup_lazy_2(self):
        self.assertEqual(zz.chainup_lazy(([1], (2, 3), [4], [], [5, 6])).list(), [1, 2, 3, 4, 5, 6])

    def test_chainup_lazy_3(self):
        n = [0]
        def foo():
            for i in zz.count(0):
                n[0] += 1
                yield [n[0], n[0]]
        arg = zz.chainup_lazy(foo())
        self.assertEqual(n, [0]) # chainup_lazy shouldn't have run foo() yet
        self.assertEqual(arg.take(5).list(), [1, 1, 2, 2, 3])
        self.assertEqual(n, [3])

    def test_zipup_longest_1(self):
        iterable = zz.zipup_longest([1, 2], ["A", "B"])
        self.assertEqual(iterable.list(), [(1, "A"), (2, "B")])

    def test_zipup_longest_2(self):
        iterable = zz.zipup_longest([1, 2], [3, 4], [5, 6])
        self.assertEqual(iterable.list(), [(1, 3, 5), (2, 4, 6)])

    def test_zipup_longest_3(self):
        iterable = zz.zipup_longest([1], [2, 3])
        self.assertEqual(iterable.list(), [(1, 2), (None, 3)])

    def test_zipup_longest_4(self):
        iterable = zz.zipup_longest([1, 2], [3])
        self.assertEqual(iterable.list(), [(1, 3), (2, None)])

    def test_zipup_longest_5(self):
        iterable = zz.zipup_longest([], ())
        self.assertTrue(iterable.null())

    def test_zipup_longest_6(self):
        iterable = zz.zipup_longest()
        self.assertTrue(iterable.null())

    def test_zipup_longest_7(self):
        iterable = zz.zipup_longest([1], [2, 3], [4], fillvalue = 9)
        self.assertEqual(iterable.list(), [(1, 2, 4), (9, 3, 9)])
