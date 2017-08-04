
from functools import reduce

def compose(*fs):
    """Composes a sequence of functions together."""
    return reduce(lambda g, h: lambda *a, **k: g(h(*a, **k)), fs)

def setindex(object, index, value):
    """Assigns a value to the specified index, using [] indexing."""
    object[index] = value

def getindex(object, index):
    """Returns the value at the specified index. This is provided for
    symmetry with setindex().

    """
    return object[index]

def delindex(object, index):
    """Deletes the value at the specified index."""
    del object[index]

def raise_(exception = None):
    """Raises an exception. This works very similarly to the raise
    statement except it is a function and thus an expression. For
    maximum compatibility between Python 2 and 3, raise_() takes at
    most one argument and does not support the "raise from" syntax or
    the 3-argument raise statement form. See the following example use
    case, which is a frequent idiom in Ruby and Perl but is not
    possible by default in Python, due to its statement rules.

    result = do_some_work() or raise_(Exception("Error: work failed"))

    do_some_work() would be a function which returns None if it fails
    or the result if it succeeds. So the exception is raised if the
    function fails.

    """
    if exception is None:
        raise
    else:
        raise exception
