
from functools import reduce

def compose(*fs):
    return reduce(lambda g, h: lambda *a, **k: g(h(*a, **k)), fs)
