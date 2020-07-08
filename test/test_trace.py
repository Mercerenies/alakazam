
from io import StringIO
import unittest
from unittest import mock
import alakazam as zz

class NullStream(object):

    def write(self, arg):
        pass

class CustomStr(object):

    def __str__(self):
        return "CustomStr.__str__"

    def __repr__(self):
        return "CustomStr.__repr__"

class TraceTest(unittest.TestCase):

    def test_trace_1(self):
        with mock.patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            zz.trace("foo", None)
            zz.trace("bar", None)
            zz.trace(900, None)
            self.assertEqual(mock_stdout.getvalue(), "foo\nbar\n900\n")

    def test_trace_2(self):
        with mock.patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            zz.trace(CustomStr(), None)
            self.assertEqual(mock_stdout.getvalue(), str(CustomStr()) + "\n")

    def test_trace_3(self):
        with mock.patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            zz.trace("foo", None, end='')
            zz.trace("bar", None, end='***')
            self.assertEqual(mock_stdout.getvalue(), "foobar***")

    def test_trace_4(self):
        stream = NullStream()
        with mock.patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            zz.trace("foo", None, file=stream)
            zz.trace("bar", None, file=stream)
            self.assertEqual(mock_stdout.getvalue(), "")

    def test_trace_5(self):
        with mock.patch('sys.stdout', new_callable=NullStream):
            self.assertEqual(zz.trace("foo", None), None)
            self.assertEqual(zz.trace("bar", 10), 10)
            self.assertEqual(zz.trace("baz", "STRING", end='\n\n\n'), "STRING")

    def test_trace_id_1(self):
        with mock.patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            zz.traceid("foo")
            zz.traceid("bar")
            zz.traceid(900)
            self.assertEqual(mock_stdout.getvalue(), "foo\nbar\n900\n")

    def test_trace_id_2(self):
        with mock.patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            zz.traceid(CustomStr())
            self.assertEqual(mock_stdout.getvalue(), str(CustomStr()) + "\n")

    def test_trace_id_3(self):
        with mock.patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            zz.traceid("foo", end='')
            zz.traceid("bar", end='***')
            self.assertEqual(mock_stdout.getvalue(), "foobar***")

    def test_trace_id_4(self):
        stream = NullStream()
        with mock.patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            zz.traceid("foo", file=stream)
            zz.traceid("bar", file=stream)
            self.assertEqual(mock_stdout.getvalue(), "")

    def test_trace_id_5(self):
        with mock.patch('sys.stdout', new_callable=NullStream):
            self.assertEqual(zz.traceid("foo"), "foo")
            self.assertEqual(zz.traceid(10), 10)
            self.assertEqual(zz.traceid("STRING", end='\n\n\n'), "STRING")

    def test_tracestack_1(self):
        # Not going to test the exact output (that's Python's problem,
        # not mine). But it should definitely output *something*
        with mock.patch('sys.stderr', new_callable=StringIO) as mock_stderr:
            zz.tracestack(None)
            self.assertTrue(mock_stderr.getvalue())

    def test_tracestack_2(self):
        with mock.patch('sys.stderr', new_callable=NullStream):
            self.assertEqual(zz.tracestack(None), None)
            self.assertEqual(zz.tracestack(100), 100)
            self.assertEqual(zz.tracestack((1, 2, 3)), (1, 2, 3))
