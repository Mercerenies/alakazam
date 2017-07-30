
class Anon:

    def __init__(self, func):
        self.__function = func

    def __call__(self, *args, **kwargs):
        return self.__function(*args, **kwargs)

    # Warning: This one will fail if the argument object does not have a __dict__
    def __getattr__(self, prop):
        return _anon_map(lambda x, p: x.__dict__[p], self, prop)

    def __getitem__(self, key):
        return _anon_map(lambda x, k: x[k], self, key)

    def __add__(self, x):
        return _anon_map(lambda s, x: s + x, self, x)

    def __sub__(self, x):
        return _anon_map(lambda s, x: s - x, self, x)

    def __mul__(self, x):
        return _anon_map(lambda s, x: s * x, self, x)

    def __truediv__(self, x):
        return _anon_map(lambda s, x: s / x, self, x)

    def __floordiv__(self, x):
        return _anon_map(lambda s, x: s // x, self, x)

    def __mod__(self, x):
        return _anon_map(lambda s, x: s % x, self, x)

    def __pow__(self, x):
        return _anon_map(lambda s, x: s ** x, self, x)

    def __lshift__(self, x):
        return _anon_map(lambda s, x: s << x, self, x)

    def __rshift__(self, x):
        return _anon_map(lambda s, x: s >> x, self, x)

    def __and__(self, x):
        return _anon_map(lambda s, x: s & x, self, x)

    def __xor__(self, x):
        return _anon_map(lambda s, x: s ^ x, self, x)

    def __or__(self, x):
        return _anon_map(lambda s, x: s | x, self, x)

    def __radd__(self, x):
        return _anon_map(lambda x, s: x + s, x, self)

    def __rsub__(self, x):
        return _anon_map(lambda x, s: x - s, x, self)

    def __rmul__(self, x):
        return _anon_map(lambda x, s: x * s, x, self)

    def __rtruediv__(self, x):
        return _anon_map(lambda x, s: x / s, x, self)

    def __rfloordiv__(self, x):
        return _anon_map(lambda x, s: x // s, x, self)

    def __rmod__(self, x):
        return _anon_map(lambda x, s: x % s, x, self)

    def __rpow__(self, x):
        return _anon_map(lambda x, s: x ** s, x, self)

    def __rlshift__(self, x):
        return _anon_map(lambda x, s: x << s, x, self)

    def __rrshift__(self, x):
        return _anon_map(lambda x, s: x >> s, x, self)

    def __rand__(self, x):
        return _anon_map(lambda x, s: x & s, x, self)

    def __rxor__(self, x):
        return _anon_map(lambda x, s: x ^ s, x, self)

    def __ror__(self, x):
        return _anon_map(lambda x, s: x | s, x, self)

    def __neg__(self):
        return _anon_map(lambda s: - s, self)

    def __pos__(self):
        return _anon_map(lambda s: + s, self)

    def __invert__(self):
        return _anon_map(lambda s: ~ s, self)

    def __eq__(self, x):
        return _anon_map(lambda s, x: s == x, self, x)

    def __ne__(self, x):
        return _anon_map(lambda s, x: s != x, self, x)

    def __lt__(self, x):
        return _anon_map(lambda s, x: s <  x, self, x)

    def __le__(self, x):
        return _anon_map(lambda s, x: s <= x, self, x)

    def __gt__(self, x):
        return _anon_map(lambda s, x: s >  x, self, x)

    def __ge__(self, x):
        return _anon_map(lambda s, x: s >= x, self, x)



# Magic methods not overriden:
#
# __init__, __call__, __new__
# * Has specific behavior for Anon
#
# __str__, __repr__, __bytes__, __format__, __iter__, __next__, __reversed__, __dir__, __len__
# __divmod__, __rdivmod__, __abs__, __complex__, __int__, __float__, __round__, __ceil__,
# __floor__, __trunc__, __copy__, __deepcopy__, __getstate__, __reduce__, __reduce_ex__,
# __getnewargs__, __setstate__, __hash__
# * For consistency with non-magic functions, prefix functions are not treated specially
#
# __contains__, __index__, __bool__, __instancecheck__, __subclasscheck__, __subclasshook__
# * Python imposes special requirements on return type that render an override of this unhelpful
#
# __setattr__, __delattr__, __setitem__, __delitem__, __iadd__, __isub__, __imul__, __itruediv__,
# __ifloordiv__, __imod__, __ipow__, __ilshift__, __irshift__, __iand__, __ixor__, __ior__,
# __enter__, __exit__, __del__, __set__, __get__
# * Overrides would not be useful since the corresponding statement is not an expression
#
# __getattribute__, __slots__, __dict__
# * Would cause more problems than it's worth
#
# __missing__
# * Unnecessary since Anon is not a dict
#
# a[_1] requires var() wrapping
# Chained comparisons cannot be used with lambda operators

def _anon_guard(anon):
    if isinstance(anon, Anon):
        return anon
    else:
        return Anon(lambda *args, **kwargs: anon)

def _anon_map(f, *anon):
    anon1 = list(map(_anon_guard, anon))
    return Anon(lambda *a, **k: f(*map(lambda x: x(*a, **k), anon1)))

def var(x):
    return Anon(lambda *args, **kwargs: x)

def arg(n):
    return Anon(lambda *args, **kwargs: args[n - 1])

def kwarg(k):
    return Anon(lambda *args, **kwargs: kwargs[k])

_1 = arg(1)
_2 = arg(2)
_3 = arg(3)
_4 = arg(4)
_5 = arg(5)
