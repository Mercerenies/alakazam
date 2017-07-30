
import itertools
import functools

from .util import *

class Alakazam:

    ## Initialization ##

    def __init__(self, iterable):
        self.value = iterable

    ## Delegation to the inner object ##

    def __iter__(self):
        return iter(self.value)

    def __str__(self):
        return "Alakazam({})".format(str(self.value))

    def __repr__(self):
        return "Alakazam({})".format(repr(self.value))

    ## Transformers that return a new Alakazam ##

    def map(self, func):
        return Alakazam(map(func, self))

    def filter(self, func):
        return Alakazam(filter(func, self))

    def islice(self, *args):
        return Alakazam(itertools.islice(self, *args))

    def take(self, n):
        return self.islice(n)

    def drop(self, n):
        return self.islice(n, None)

    def accumulate(self, func = None):
        if func is None:
            return Alakazam(itertools.accumulate(self))
        else:
            return Alakazam(itertools.accumulate(self, func))

    def chain(self, *args):
        return Alakazam(itertools.chain(self, *args))

    def chain_lazy(self, iterable):
        temp = itertools.chain(self, itertools.chain.from_iterable(iterable))
        return Alakazam(temp)

    def compress(self, sel):
        return Alakazam(itertools.compress(self, sel))

    def dropwhile(self, pred):
        return Alakazam(itertools.dropwhile(pred, self))

    def filterfalse(self, pred):
        return Alakazam(itertools.filterfalse(pred, self))

    def groupby(self, key = None):
        def grouper():
            for k, g in itertools.groupby(self, key):
                yield k, list(g)
        return Alakazam(grouper())

    def starmap(self, func):
        return Alakazam(itertools.starmap(func, self))

    def takewhile(self, pred):
        return Alakazam(itertools.takewhile(pred, self))

    def enumerate(self, start = 0):
        return Alakazam(enumerate(self, start))

    def group(self, n):
        return (self
                .enumerate()
                .groupby(lambda x: x[0] // n)
                .map(lambda x: x[1])
                .map(lambda x: list(map(lambda y: y[1], x))))

    def zip(self, *args):
        return Alakazam(zip(self, *args))

    def zip_longest(self, fillvalue = None, *args):
        return Alakazam(itertools.zip_longest(self, *args, fillvalue = fillvalue))

    def cross_product(self, repeat = 1, *args):
        return Alakazam(itertools.product(self, *args, repeat = repeat))

    def permutations(self, r = None):
        return Alakazam(itertools.permutations(self, r))

    def combinations(self, r):
        return Alakazam(itertools.combinations(self, r))

    def combinations_with_replacement(self, r):
        return Alakazam(itertools.combinations_with_replacement(self, r))

    def reversed(self):
        return Alakazam(reversed(self.value))

    ## Generators that construct a Alakazam sequence ##

    @staticmethod
    def count(start, step = 1):
        return Alakazam(itertools.count(start, step))

    @staticmethod
    def cycle(p):
        return Alakazam(itertools.cycle(p))

    @staticmethod
    def repeat(elem, n = None):
        if n is None:
            return Alakazam(itertools.repeat(elem))
        else:
            return Alakazam(itertools.repeat(elem, n))

    @staticmethod
    def of(value):
        return Alakazam(value)

    @staticmethod
    def range(*args):
        return Alakazam(range(*args))

    ## Reducers that return a scalar ##

    def reduce(self, func, init = None):
        if init is None:
            return functools.reduce(func, self)
        else:
            return functools.reduce(func, self, init)

    def foldl(self, func, init = None):
        return self.reduce(func, init)

    def foldr(self, func, init = None):
        return self.foldr_lazy(lambda x, y: func(x, y()), init)

    def foldr_lazy(self, func, init = None):
        def _recurse(acc, iterable):
            try:
                arg = next(iterable)
            except StopIteration:
                if init is None:
                    return acc
                else:
                    return func(acc, lambda: init)
            return func(acc, lambda: _recurse(arg, iterable))
        iterable = iter(self)
        try:
            arg = next(iterable)
        except StopIteration:
            if init is None:
                raise TypeError("foldr() of empty sequence with no initial value")
            else:
                return init
        return _recurse(arg, iterable)

    def sum(self, init = 0):
        return sum(self, init)

    def product(self, init = 1):
        return functools.reduce(lambda x, y: x * y, self, init)

    def find(self, func, default = None):
        for x in self:
            if func(x): return x
        return default

    def all(self, func = None):
        if func is None: func = lambda x: x
        notfound = object()
        result = self.find(lambda x: not func(x), default = notfound)
        return result is notfound

    def any(self, func = None, default = False):
        if func is None: func = lambda x: x
        return self.map(func).find(lambda x: x, default = default)

    ## Simplifiers that return another iterable or container type ##

    def list(self):
        return list(self)

    def tuple(self):
        return tuple(self)

    def set(self):
        return set(self)

    def dict(self, **kwargs):
        return dict(self, **kwargs)

    ## Miscellaneous ##

    def tee(self, n = 2):
        return tuple(map(Alakazam, itertools.tee(self, n)))

ZZ = Alakazam
