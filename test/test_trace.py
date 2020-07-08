
from io import StringIO, BytesIO
import unittest
import alakazam as zz
import sys

class Patched:

    def __init__(self, stream_name):
        self.old_stream = None
        self.stream_name = stream_name

    def __enter__(self):
        if sys.version_info >= (3, 0):
            stream = StringIO()
        else:
            stream = BytesIO()
        self.old_stream = sys.__dict__[self.stream_name]
        sys.__dict__[self.stream_name] = stream
        return stream

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.__dict__[self.stream_name] = self.old_stream
        return False

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
        with Patched('stdout') as mock_stdout:
            zz.trace("foo", None)
            zz.trace("bar", None)
            zz.trace(900, None)
            self.assertEqual(mock_stdout.getvalue(), "foo\nbar\n900\n")

    def test_trace_2(self):
        with Patched('stdout') as mock_stdout:
            zz.trace(CustomStr(), None)
            self.assertEqual(mock_stdout.getvalue(), str(CustomStr()) + "\n")

    def test_trace_3(self):
        with Patched('stdout') as mock_stdout:
            zz.trace("foo", None, end='')
            zz.trace("bar", None, end='***')
            self.assertEqual(mock_stdout.getvalue(), "foobar***")

    def test_trace_4(self):
        stream = NullStream()
        with Patched('stdout') as mock_stdout:
            zz.trace("foo", None, file=stream)
            zz.trace("bar", None, file=stream)
            self.assertEqual(mock_stdout.getvalue(), "")

    def test_trace_5(self):
        with Patched('stdout'):
            self.assertEqual(zz.trace("foo", None), None)
            self.assertEqual(zz.trace("bar", 10), 10)
            self.assertEqual(zz.trace("baz", "STRING", end='\n\n\n'), "STRING")

    def test_trace_id_1(self):
        with Patched('stdout') as mock_stdout:
            zz.traceid("foo")
            zz.traceid("bar")
            zz.traceid(900)
            self.assertEqual(mock_stdout.getvalue(), "foo\nbar\n900\n")

    def test_trace_id_2(self):
        with Patched('stdout') as mock_stdout:
            zz.traceid(CustomStr())
            self.assertEqual(mock_stdout.getvalue(), str(CustomStr()) + "\n")

    def test_trace_id_3(self):
        with Patched('stdout') as mock_stdout:
            zz.traceid("foo", end='')
            zz.traceid("bar", end='***')
            self.assertEqual(mock_stdout.getvalue(), "foobar***")

    def test_trace_id_4(self):
        stream = NullStream()
        with Patched('stdout') as mock_stdout:
            zz.traceid("foo", file=stream)
            zz.traceid("bar", file=stream)
            self.assertEqual(mock_stdout.getvalue(), "")

    def test_trace_id_5(self):
        with Patched('stdout'):
            self.assertEqual(zz.traceid("foo"), "foo")
            self.assertEqual(zz.traceid(10), 10)
            self.assertEqual(zz.traceid("STRING", end='\n\n\n'), "STRING")

    def test_tracestack_1(self):
        # Not going to test the exact output (that's Python's problem,
        # not mine). But it should definitely output *something*
        with Patched('stderr') as mock_stderr:
            zz.tracestack(None)
            self.assertTrue(mock_stderr.getvalue())

    def test_tracestack_2(self):
        with Patched('stderr'):
            self.assertEqual(zz.tracestack(None), None)
            self.assertEqual(zz.tracestack(100), 100)
            self.assertEqual(zz.tracestack((1, 2, 3)), (1, 2, 3))
