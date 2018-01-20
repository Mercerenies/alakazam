
from .error import *
from .anonymous import *

class PatternClass(type):

    def __new__(cls, name, parents, dct):
        return type.__new__(cls, name, parents, dct)

    def __getitem__(self, args):
        def pattern(*iargs):
            return self.zz_apply(*iargs)
        binder = bind(pattern)(*args)
        return binder

def pattern_class(cls):
    return PatternClass(cls.__name__, (cls,), {})

@pattern_class
class Tup(object):
    def zz_apply(*args):
        return tuple(args)



