
import unittest
import alakazam as zz

class ConversionTest(unittest.TestCase):

    def test_subclass_1(self):
        self.assertTrue(issubclass(zz.Alakazam, object))

    def test_subclass_2(self):
        self.assertTrue(issubclass(zz.Anon, object))
