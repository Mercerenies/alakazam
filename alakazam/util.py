
from functools import reduce

def id(x):
    """Returns the argument without modification."""
    return x

def compose(*fs):
    """Composes a sequence of functions together."""
    return reduce(lambda g, h: lambda *a, **k: g(h(*a, **k)), fs, id)

def swap(arg):
    """Swaps the first two elements of the tuple."""
    def index(x):
        return 1 - x if x < 2 else x
    return tuple(arg[index(n)] for n in range(len(arg)))

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

def not_(x):
    """Returns the Boolean negation of the argument."""
    return not x

def and_(*xs):
    """Returns the first falsy value among the arguments, or the final
    argument if all values are truthy. If no arguments are provided,
    True is returned.

    """
    final = True
    for x in xs:
        if not x:
            return x
        final = x
    return final

def or_(*xs):
    """Returns the first truthy value among the arguments, or the final
    argument if all values are falsy. If no arguments are provided,
    False is returned.

    """
    final = False
    for x in xs:
        if x:
            return x
        final = x
    return final

def xor(*xs):
    """Normalizes all of the arguments to Boolean values and then returns
    the Boolean exclusive-or of all the values. Specifically, this
    function returns True if and only if an odd number of the
    arguments are truthy and False otherwise.

    """
    final = False
    for x in xs:
        if x:
            final = not final
    return final

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
