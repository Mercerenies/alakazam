
from .error import *
from .anonymous import *

zero = object()

class etc(object):

    def __init__(self, name):
        self.name = name

def _is_etc(obj):
    return obj is Ellipsis or isinstance(obj, etc)

def _etc_name(obj):
    if isinstance(obj, etc):
        return obj.name
    else:
        return None

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
        binder._Anon__pattern = pattern
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
