
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
