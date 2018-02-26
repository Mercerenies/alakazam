
import operator
import unittest
import alakazam as zz

class TransformerTest(unittest.TestCase):

    def test_map_1(self):
        self.assertEqual(zz.range(0, 5).map(lambda x: x + 1).list(), list(range(1, 6)))

    def test_map_2(self):
        # map should be lazy
        self.assertEqual(zz.count(0).map(lambda x: x + 1).take(5).list(), list(range(1, 6)))

    def test_filter_1(self):
        self.assertEqual(zz.range(0, 10).filter(lambda x: x % 2 == 1).list(), [1, 3, 5, 7, 9])

    def test_filter_2(self):
        # filter should be lazy
        self.assertEqual(zz.count(0).filter(lambda x: x % 2 == 1).take(5).list(), [1, 3, 5, 7, 9])

    def test_islice_1(self):
        self.assertEqual(zz.range(10).islice(5).list(), [0, 1, 2, 3, 4])

    def test_islice_2(self):
        self.assertEqual(zz.range(10).islice(1, 5).list(), [1, 2, 3, 4])

    def test_islice_3(self):
        self.assertEqual(zz.range(10).islice(1, 5, 2).list(), [1, 3])

    def test_islice_4(self):
        self.assertEqual(zz.range(10).islice(5, None, 2).list(), [5, 7, 9])

    def test_take_1(self):
        self.assertEqual(zz.range(10).take(2).list(), [0, 1])

    def test_take_2(self):
        # Should handle out-of-bounds by truncating
        self.assertEqual(zz.range(3).take(99).list(), [0, 1, 2])

    def test_take_3(self):
        self.assertTrue(zz.range(10).take(0).null())

    def test_take_4(self):
        # Works on infinite lists
        self.assertEqual(zz.repeat(7).take(2).list(), [7, 7])

    def test_drop_1(self):
        self.assertEqual(zz.range(10).drop(5).list(), [5, 6, 7, 8, 9])

    def test_drop_2(self):
        # Should handle out-of-bounds by truncating
        self.assertTrue(zz.range(3).drop(99).null())

    def test_drop_3(self):
        self.assertEqual(zz.range(10).drop(0).list(), list(range(10)))

    def test_drop_4(self):
        # Works on infinite lists
        self.assertEqual(zz.count(1).drop(2).take(3).list(), [3, 4, 5])

    def test_accumulate_1(self):
        self.assertEqual(zz.count(0).accumulate().take(5).list(), [0, 1, 3, 6, 10])

    def test_accumulate_2(self):
        self.assertEqual(zz.count(1).accumulate(operator.mul).take(5).list(), [1, 2, 6, 24, 120])

    def test_accumulate_3(self):
        self.assertEqual(zz.count(1).accumulate(operator.mul, init = 1).take(5).list(), [1, 1, 2, 6, 24])

    def test_accumulate_4(self):
        self.assertEqual(zz.empty().accumulate(init = None).list(), [None])

    def test_accumulate_4(self):
        self.assertTrue(zz.empty().accumulate().null())

    def test_chain_1(self):
        self.assertEqual(zz.of([1, 2, 3]).chain([4, 5, 6]).list(), list(range(1, 7)))

    def test_chain_2(self):
        self.assertEqual(zz.of([1, 2, 3]).chain([4], [5], [6]).list(), list(range(1, 7)))

    def test_chain_3(self):
        self.assertEqual(zz.of([1, 2, 3]).chain().list(), list(range(1, 4)))

    def test_chain_4(self):
        # chain is lazy
        self.assertEqual(zz.of([1, 2, 3]).chain(zz.count(0), [-1]).take(5).list(), [1, 2, 3, 0, 1])

    def test_chain_lazy_1(self):
        self.assertEqual(zz.of([1, 2, 3]).chain_lazy([[4, 5, 6]]).list(), list(range(1, 7)))

    def test_chain_lazy_2(self):
        self.assertEqual(zz.of([1, 2, 3]).chain_lazy(([4], [5], [6])).list(), list(range(1, 7)))

    def test_chain_lazy_3(self):
        # chain is lazy
        self.assertEqual(zz.of([1, 2, 3]).chain_lazy(()).list(), list(range(1, 4)))

    def test_chain_lazy_4(self):
        # chain is lazy
        def foo():
            arr = []
            for i in zz.count(1):
                arr.append(i)
                yield arr
        self.assertEqual(zz.of([9, 9, 9]).chain_lazy(foo()).take(9).list(), [9, 9, 9, 1, 1, 2, 1, 2, 3])

    def test_compress_1(self):
        self.assertEqual(zz.range(4).compress([1, 0, 1, 0]).list(), [0, 2])

    def test_compress_2(self):
        self.assertEqual(zz.range(10).compress([1, 0, 1, 0]).list(), [0, 2])

    def test_compress_3(self):
        self.assertEqual(zz.range(4).compress([1, 0, 1, 0, 1, 0]).list(), [0, 2])

    def test_dropwhile_1(self):
        self.assertEqual(zz.range(1, 10).dropwhile(lambda x: x % 3 != 0).list(), list(range(3, 10)))

    def test_dropwhile_2(self):
        # Works on infinite lists
        self.assertEqual(zz.count(1).dropwhile(lambda x: x % 3 != 0).take(3).list(), [3, 4, 5])

    def test_filterfalse_1(self):
        self.assertEqual(zz.range(0, 10).filterfalse(lambda x: x % 2 == 1).list(), [0, 2, 4, 6, 8])

    def test_filterfalse_2(self):
        # filterfalse should be lazy
        self.assertEqual(zz.count(0).filterfalse(lambda x: x % 2 == 1).take(5).list(), [0, 2, 4, 6, 8])

    def test_groupby_1(self):
        self.assertEqual(zz.of([0, 0, 1, 1, 0, 0, 1, 1]).groupby().tuple(), ((0, [0, 0]), (1, [1, 1]), (0, [0, 0]), (1, [1, 1])))

    def test_groupby_2(self):
        self.assertEqual(zz.range(10).groupby(key = lambda x: x // 3).tuple(), ((0, [0, 1, 2]), (1, [3, 4, 5]), (2, [6, 7, 8]), (3, [9])))

    def test_groupby_3(self):
        self.assertEqual(zz.count(0).groupby(key = lambda x: x // 3).take(4).tuple(), ((0, [0, 1, 2]), (1, [3, 4, 5]), (2, [6, 7, 8]), (3, [9, 10, 11])))

    def test_starmap_1(self):
        self.assertEqual(zz.of(((10, 15), (20, 25))).starmap(operator.add).list(), [25, 45])

    def test_starmap_2(self):
        # starmap should be lazy
        self.assertEqual(zz.repeat((1, 1)).starmap(operator.add).take(3).list(), [2, 2, 2])

    def test_takewhile_1(self):
        self.assertEqual(zz.range(1, 10).takewhile(lambda x: x % 4 != 0).list(), [1, 2, 3])

    def test_takewhile_2(self):
        # Works on infinite lists
        self.assertEqual(zz.count(1).takewhile(lambda x: x % 4 != 0).take(3).list(), [1, 2, 3])

    def test_enumerate_1(self):
        self.assertEqual(zz.of([10, 9, 8]).enumerate().list(), [(0, 10), (1, 9), (2, 8)])

    def test_enumerate_2(self):
        self.assertEqual(zz.of([10, 9, 8]).enumerate(start = 9).list(), [(9, 10), (10, 9), (11, 8)])

    def test_enumerate_3(self):
        # Works on infinite lists
        self.assertEqual(zz.count(10).enumerate().take(2).list(), [(0, 10), (1, 11)])

    def test_group_1(self):
        self.assertEqual(zz.range(10).group(3).list(), [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]])

    def test_group_2(self):
        self.assertEqual(zz.count(0).group(4).take(2).tuple(), ([0, 1, 2, 3], [4, 5, 6, 7]))

    def test_zip_1(self):
        iterable = zz.of([1, 2]).zip(["A", "B"])
        self.assertEqual(iterable.list(), [(1, "A"), (2, "B")])

    def test_zip_2(self):
        iterable = zz.of([1, 2]).zip([3, 4], [5, 6])
        self.assertEqual(iterable.list(), [(1, 3, 5), (2, 4, 6)])

    def test_zip_3(self):
        iterable = zz.of([1]).zip([3, 4], [5, 6])
        self.assertEqual(iterable.list(), [(1, 3, 5)])

    def test_zip_4(self):
        iterable = zz.of([1, 2]).zip([3], [5, 6])
        self.assertEqual(iterable.list(), [(1, 3, 5)])

    def test_zip_5(self):
        iterable = zz.of([1, 2]).zip([3, 4], [5])
        self.assertEqual(iterable.list(), [(1, 3, 5)])

    def test_zip_6(self):
        # Make sure it works given no arguments
        iterable = zz.of([1, 2]).zip()
        self.assertEqual(iterable.list(), [(1,), (2,)])

    def test_zip_7(self):
        iterable = zz.count(0).zip(range(2))
        self.assertEqual(iterable.list(), [(0, 0), (1, 1)])

    def test_zip_8(self):
        iterable = zz.repeat(1).zip(zz.repeat(2))
        self.assertEqual(iterable.take(2).list(), [(1, 2), (1, 2)])

    def test_zip_longest_1(self):
        iterable = zz.of([1, 2]).zip_longest(["A", "B"])
        self.assertEqual(iterable.list(), [(1, "A"), (2, "B")])

    def test_zip_longest_2(self):
        iterable = zz.of([1, 2]).zip_longest([3, 4], [5, 6])
        self.assertEqual(iterable.list(), [(1, 3, 5), (2, 4, 6)])

    def test_zip_longest_3(self):
        iterable = zz.of([1]).zip_longest([3, 4], [5, 6])
        self.assertEqual(iterable.list(), [(1, 3, 5), (None, 4, 6)])

    def test_zip_longest_4(self):
        iterable = zz.of([1, 2]).zip_longest([3], [5, 6])
        self.assertEqual(iterable.list(), [(1, 3, 5), (2, None, 6)])

    def test_zip_longest_5(self):
        iterable = zz.of([1, 2]).zip_longest([3, 4], [5])
        self.assertEqual(iterable.list(), [(1, 3, 5), (2, 4, None)])

    def test_zip_longest_6(self):
        # Make sure it works given no arguments
        iterable = zz.of([1, 2]).zip_longest()
        self.assertEqual(iterable.list(), [(1,), (2,)])

    def test_zip_longest_7(self):
        iterable = zz.of([1, 2]).zip_longest([3], [5], fillvalue = -1)
        self.assertEqual(iterable.list(), [(1, 3, 5), (2, -1, -1)])

    def test_flatten_1(self):
        self.assertEqual(zz.of([[[1]], [[2]]]).flatten().list(), [[1], [2]])

    def test_flatten_2(self):
        # Works on infinite lists
        self.assertEqual(zz.count(0).map(lambda x: [x]).flatten().take(10).list(), list(range(10)))

    def test_cross_product_1(self):
        self.assertEqual(zz.of([1, 2]).cross_product([3, 4]).list(), [(1, 3), (1, 4), (2, 3), (2, 4)])

    def test_cross_product_2(self):
        self.assertEqual(zz.of([1, 2]).cross_product(repeat = 2).list(), [(1, 1), (1, 2), (2, 1), (2, 2)])

    def test_cross_product_3(self):
        self.assertEqual(zz.of([1, 2]).cross_product().list(), [(1,), (2,)])

    def test_cross_product_4(self):
        self.assertTrue(zz.of([1, 2]).cross_product(()).null())

    def test_permutations_1(self):
        self.assertEqual(zz.of([1, 2, 3]).permutations(r = 2).list(), [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)])

    def test_permutations_2(self):
        self.assertEqual(zz.of([1, 2, 3]).permutations().list(), [(1, 2, 3), (1, 3, 2), (2, 1, 3), (2, 3, 1), (3, 1, 2), (3, 2, 1)])

    def test_combinations(self):
        self.assertEqual(zz.of([1, 2, 3]).combinations(r = 2).list(), [(1, 2), (1, 3), (2, 3)])

    def test_combinations_with_replacement(self):
        self.assertEqual(zz.of([1, 2, 3]).combinations_with_replacement(r = 2).list(), [(1, 1), (1, 2), (1, 3), (2, 2), (2, 3), (3, 3)])

    def test_cycle_1(self):
        self.assertEqual(zz.range(3).cycle().take(5).list(), [0, 1, 2, 0, 1])

    def test_cycle_2(self):
        self.assertTrue(zz.empty().cycle().null())

    def test_reversed(self):
        self.assertEqual(zz.of([1, 2, 3]).reversed().list(), [3, 2, 1])

    def test_withobject_1(self):
        self.assertEqual(zz.of([1, 2, 3]).withobject(-1).list(), [(-1, 1), (-1, 2), (-1, 3)])

    def test_withobject_2(self):
        self.assertEqual(zz.count(1).withobject(-1).take(3).list(), [(-1, 1), (-1, 2), (-1, 3)])

    def test_interlace_1(self):
        self.assertEqual(zz.of([1, 2, 3]).interlace([4, 5, 6]).list(), [1, 4, 2, 5, 3, 6])

    def test_interlace_2(self):
        self.assertEqual(zz.of([1, 2]).interlace([3, 4], [5, 6]).list(), [1, 3, 5, 2, 4, 6])

    def test_interlace_3(self):
        iterable = zz.count(1, step=1).interlace(zz.count(-1, step=-1))
        self.assertEqual(iterable.take(10).list(), [1, -1, 2, -2, 3, -3, 4, -4, 5, -5])

    def test_intersperse_1(self):
        self.assertEqual(zz.of([1, 2, 3]).intersperse(999).list(), [1, 999, 2, 999, 3])

    def test_intersperse_2(self):
        self.assertEqual(zz.empty().intersperse(0).list(), [])

    def test_intersperse_3(self):
        iterable = zz.count(1, step=1).intersperse(0)
        self.assertEqual(iterable.take(10).list(), [1, 0, 2, 0, 3, 0, 4, 0, 5, 0])
