
import unittest
import alakazam as zz

class MagicTest(unittest.TestCase):

    def test_iter(self):
        arg1 = iter([10])
        arg2 = zz.of(arg1)
        self.assertEqual(iter(arg1), iter(arg2))

    def test_reversed(self):
        self.assertEqual(list(reversed(zz.of([1, 2, 3]))), [3, 2, 1])

    def test_len(self):
        self.assertEqual(len(zz.range(10)), 10)
