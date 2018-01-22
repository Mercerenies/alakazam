
from .error import *
from .anonymous import *

zero = object()

class etc(object):

    def __init__(self, name):
        self.name = name

class PatternMatch(object):

    def __init__(self):
        self.okay = True
        self.vars = {}
        self.max  = 0

    def __bool__(self):
        return self.okay

    def __nonzero__(self):
        return self.__bool__()

    def __setitem__(self, index, value):
        if index in self.vars:
            raise AlakazamError("Repeated binding in pattern")
        if isinstance(index, int):
            self.max = max(self.max, index + 1)
        self.vars[index] = value

    def __getitem__(self, index):
        return self.vars.get(index, None)

    def __delitem__(self, index):
        if index in self.vars:
            del self.vars[index]

    def fail(self):
        self.okay = False

    def build_args(self):
        if not self:
            return None
        tup = tuple(self[i] for i in range(self.max))
        kw = dict((key, self.vars[key]) for key in self.vars if isinstance(key, str))
        return (tup, kw)

    def call(self, func):
        if self:
            args, kwargs = self.build_args()
            return func(*args, **kwargs)
        else:
            raise AlakazamError("Cannot call on failed pattern match")

def _is_etc(obj):
    return obj is Ellipsis or isinstance(obj, etc)

def _etc_name(obj):
    if isinstance(obj, etc):
        return obj.name
    else:
        return None

def _match_impl_seq(res, ptn, obj):
    try:
        curr = next(ptn)
    except StopIteration:
        # End of pattern; we should also be at the end of object sequence
        try:
            next(obj)
        except StopIteration:
            pass
        else:
            res.fail()
        return
    if _is_etc(curr):
        # Matches the rest automatically
        if _etc_name(curr) is not None:
            _match_impl(res, _etc_name(curr), obj)
        return
    try:
        test = next(obj)
    except StopIteration:
        # Out of objects but still have a pattern; oops
        res.fail()
        return
    _match_impl(res, curr, test)
    _match_impl_seq(res, ptn, obj)

def _match_impl(res, ptn, obj):
    if isinstance(ptn, Anon):
        if not ptn._Anon__pattern:
            raise AlakazamError("Non-pattern expression in pattern context")
        new_ptn, test = ptn._Anon__pattern
        if callable(test):
            # It's a function; recurse
            subobj = test(obj)
            if subobj is None:
                res.fail()
            else:
                _match_impl_seq(res, iter(new_ptn), iter(subobj))
        else:
            res[test] = obj
    else:
        # It's a literal; compare for equality
        if ptn != obj:
            res.fail()

def match(ptn, obj):
    res = PatternMatch()
    _match_impl(res, ptn, obj)
    return res

def let(*args):
    # let(ptn, obj, func)
    # let(match_obj, func)
    if len(args) == 3:
        ptn, obj, func = args
        return let(match(ptn, obj), func)
    else:
        match_expr, func = args
        if match_expr:
            return match_expr.call(func)
        else:
            raise AlakazamError("let-expression on failed pattern match")

class PatternClass(type):

    def __new__(cls, name, parents, dct):
        return type.__new__(cls, name, parents, dct)

    def __getitem__(self, args):

        def call(*iargs):
            return self.zz_apply(*iargs)
        def pattern(arg):
            return self.zz_unapply(arg)

        if not isinstance(args, tuple):
            args = (args,)
        if args == (zero,):
            args = ()
        binder = bind(call)(*args)
        binder._Anon__pattern = (args, pattern)
        return binder

def pattern_class(cls):
    return PatternClass(cls.__name__, (cls,), {})

@pattern_class
class Tup(object):
    def zz_apply(*args):
        return tuple(args)
    def zz_unapply(arg):
        if not isinstance(arg, tuple):
            return None
        return arg
