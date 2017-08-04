
import itertools
import functools
import sys

from .util import *

class Alakazam:

    ## Initialization ##

    def __init__(self, iterable):
        """Constructs an Alakazam instance wrapping the given iterable."""
        self.value = iterable

    ## Delegation to the inner object ##

    def __iter__(self):
        return iter(self.value)

    def __reversed__(self):
        return reversed(self.value)

    def __len__(self):
        return len(self.value)

    def __str__(self):
        return "Alakazam({})".format(str(self.value))

    def __repr__(self):
        return "Alakazam({})".format(repr(self.value))

    ## Transformers that return a new Alakazam ##

    def map(self, func):
        """Maps a function over each element."""
        return Alakazam(map(func, self))

    def filter(self, func):
        """Retains only elements for which the function returns true."""
        return Alakazam(filter(func, self))

    def islice(self, *args):
        """Slices the Alakazam iterable, as if through itertools.islice."""
        return Alakazam(itertools.islice(self, *args))

    def take(self, n):
        """Retains only the first N elements of the iterable."""
        return self.islice(n)

    def drop(self, n):
        """Eliminates the first N elements of the iterable."""
        return self.islice(n, None)

    def accumulate(self, func = None):
        """Accumulates the elements of the list, using the given function or
        the __add__ operator. This method behaves identically to the
        itertools.accumulate method.

        """

        if func is None:
            return Alakazam(itertools.accumulate(self))
        else:
            return Alakazam(itertools.accumulate(self, func))

    def chain(self, *args):
        """Chains the iterables together, with the Alakazam iterable at the front."""
        return Alakazam(itertools.chain(self, *args))

    def chain_lazy(self, iterable):
        """Chains the iterables within the argument together, with the
        Alakazam iterable at the front.

        """
        temp = itertools.chain(self, itertools.chain.from_iterable(iterable))
        return Alakazam(temp)

    def compress(self, sel):
        """Compresses the iterable, as with itertools.compress."""
        return Alakazam(itertools.compress(self, sel))

    def dropwhile(self, pred):
        """Drops elements of the iterable until an element matching the
        predicate is found.

        """
        return Alakazam(itertools.dropwhile(pred, self))

    def filterfalse(self, pred):
        """Retains only the elements for which the predicate returns false."""
        return Alakazam(itertools.filterfalse(pred, self))

    def groupby(self, key = None):
        """Groups the elements of the iterable together, as though with
        itertools.groupby.  Because of the way Alakazam works, there
        is one subtle difference between this an itertools.groupby, in
        that this method will return a lazy iterable of grouped lists,
        while the itertools version returns a lazy iterable of lazy
        iterable groups.

        """
        def grouper():
            for k, g in itertools.groupby(self, key):
                yield k, list(g)
        return Alakazam(grouper())

    def starmap(self, func):
        """Maps a function over the iterable, passing each element as an argument list."""
        return Alakazam(itertools.starmap(func, self))

    def takewhile(self, pred):
        """Keeps elements of the iterable until the predicate returns false."""
        return Alakazam(itertools.takewhile(pred, self))

    def enumerate(self, start = 0):
        """Pairs each element of the iterable with an index value."""
        return Alakazam(enumerate(self, start))

    def group(self, n):
        """Returns a new iterable, with every N elements grouped together into
        a sublist.

        """
        return (self
                .enumerate()
                .groupby(lambda x: x[0] // n)
                .map(lambda x: x[1])
                .map(lambda x: list(map(lambda y: y[1], x))))

    def zip(self, *args):
        """Zips the Alakazam iterable with the arguments."""
        return Alakazam(zip(self, *args))

    def zip_longest(self, *args, **kwargs):
        """Zips the Alakazam iterable with the arguments, padding with fillvalue."""
        if 'fillvalue' in kwargs:
            fillvalue = kwargs['fillvalue']
        else:
            fillvalue = None
        return Alakazam(itertools.zip_longest(self, *args, fillvalue = fillvalue))

    def cross_product(self, *args, **kwargs):
        """Returns the Cartesian product, as through with itertools.product."""
        if 'repeat' in kwargs:
            repeat = kwargs['repeat']
        else:
            repeat = 1
        return Alakazam(itertools.product(self, *args, repeat = repeat))

    def permutations(self, r = None):
        """Returns all r-permutations of the Alakazam iterable's elements."""
        return Alakazam(itertools.permutations(self, r))

    def combinations(self, r):
        """Returns all r-combinations of the Alakazam iterable's elements."""
        return Alakazam(itertools.combinations(self, r))

    def combinations_with_replacement(self, r):
        """Returns all r-combinations of the Alakazam iterable's elements, with replacement."""
        return Alakazam(itertools.combinations_with_replacement(self, r))

    def cycle(self):
        """Returns an infinite stream of the elements, cyclically."""
        return Alakazam(itertools.cycle(self))

    def reversed(self):
        """Returns a reversed version of the Alakazam iterable. This is only
        meaningful if the underlying iterable can be reversed, so it
        is seldom used.

        """
        return Alakazam(reversed(self.value))

    ## Generators that construct a Alakazam sequence ##

    @staticmethod
    def count(start, step = 1):
        """Returns an infinite stream counting upward or downward, as though
        with itertools.count.

        """
        return Alakazam(itertools.count(start, step))

    @staticmethod
    def repeat(elem, n = None):
        """Repeats the element N times, or forever if N is None."""
        if n is None:
            return Alakazam(itertools.repeat(elem))
        else:
            return Alakazam(itertools.repeat(elem, n))

    @staticmethod
    def of(value):
        """Constructs an Alakazam value. This method is equivalent to calling
        the Alakazam constructor directly but sometimes looks neater
        when chaining method calls together.

        """
        return Alakazam(value)

    @staticmethod
    def of_dict(value):
        """Constructs an Alakazam value containing key-value 2-tuples."""
        if sys.version_info >= (3, 0):
            return Alakazam(value.items())
        else:
            return Alakazam(value.iteritems())


    @staticmethod
    def range(*args):
        """Returns a range() object through Alakazam."""
        return Alakazam(range(*args))

    @staticmethod
    def empty():
        """Returns an empty iterable."""
        return Alakazam(())

    ## Reducers that return a scalar ##

    def reduce(self, func, init = None):
        """Reduces the Alakazam iterable, as though with the standard
        functools.reduce.

        """
        if init is None:
            return functools.reduce(func, self)
        else:
            return functools.reduce(func, self, init)

    def foldl(self, func, init = None):
        """Reduces the Alakazam iterable from the left."""
        return self.reduce(func, init)

    def foldr(self, func, init = None):
        """Reduces the Alakazam iterable from the right."""
        return self.foldr_lazy(lambda x, y: func(x, y()), init)

    def foldr_lazy(self, func, init = None):
        """Reduces the Alakazam iterable from the right lazily. This method
        comes in handy when dealing with infinite streams. The second
        argument to the folding function is a callable object, not an
        ordinary value. When called, the object computes the remainder
        of the lazy fold. Thus, to terminate the fold early, simply do
        not call the second argument.

        """
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
        """Sums the iterable with __add__."""
        return sum(self, init)

    def product(self, init = 1):
        """Finds the product of the iterable with __mul__."""
        return functools.reduce(lambda x, y: x * y, self, init)

    def find(self, func, default = None):
        """Returns the first element of the iterable for which the function
        returns true, or the default value if no such element is found.

        """
        for x in self:
            if func(x): return x
        return default

    def all(self, func = None):
        """Returns whether the function is true for all elements in the
        iterable. The function defaults to the identity function.

        """
        if func is None: func = lambda x: x
        notfound = object()
        result = self.find(lambda x: not func(x), default = notfound)
        return result is notfound

    def any(self, func = None, default = False):
        """Returns the first truthy result obtained by applying the function
        to each element of the iterable, or the default value if the
        function returns falsy for every element. The function
        argument defaults to the identity function.

        """
        if func is None: func = lambda x: x
        return self.map(func).find(lambda x: x, default = default)

    ## Simplifiers that return another iterable or container type ##

    def list(self):
        """Converts the iterable, which must be finite, to a list."""
        return list(self)

    def tuple(self):
        """Converts the iterable, which must be finite, to a tuple."""
        return tuple(self)

    def set(self):
        """Converts the iterable, which must be finite, to a set."""
        return set(self)

    def dict(self, **kwargs):
        """Converts the iterable, which must be finite and consist only of
        2-tuples, to a dict.

        """
        return dict(self, **kwargs)

    ## Miscellaneous ##

    def tee(self, n = 2):
        """Splits the iterable into multiple iterables, as though through itertools.tee."""
        return tuple(map(Alakazam, itertools.tee(self, n)))

ZZ = Alakazam

def count(start, step = 1):
    """Returns an infinite stream counting upward or downward, as though
    with itertools.count.

    """
    return ZZ.count(start, step = step)

def repeat(elem, n = None):
    """Repeats the element N times, or forever if N is None."""
    return ZZ.repeat(elem, n = n)

def of(value):
    """Constructs an Alakazam value. This method is equivalent to calling
    the Alakazam constructor directly but sometimes looks neater
    when chaining method calls together.

    """
    return ZZ.of(value)

def of_dict(value):
    """Constructs an Alakazam value containing key-value 2-tuples."""
    return ZZ.of_dict(value)

def range(*args):
    """Returns a range() object through Alakazam."""
    return ZZ.range(*args)

def empty():
    """Returns an empty iterable."""
    return ZZ.empty()
