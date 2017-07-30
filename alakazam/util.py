
from functools import reduce

def compose(*fs):
    """Composes a sequence of functions together."""
    return reduce(lambda g, h: lambda *a, **k: g(h(*a, **k)), fs)
