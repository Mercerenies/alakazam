
Alakazam
========

Functional programming sugar for Python.

Installing
----------

Instructions coming soon.

Using
-----

To use the stream functionality of Alakazam, import the ``alakazam``
package. It is recommended that you alias the package as something
like `zz` for easier typing.

To use the Alakazam lambda syntax, import the placeholders from
``alakazam`` explicitly. ::

    import alakazam as zz
    from alakazam import _1, _2, _3, _4, _5

This library aims to make functional-style, and specifically
stream-oriented programming in Python prettier, more pleasant, and
easier on the eyes. Python has been capable of many functional
programming tasks, but it has always been a little bit awkward to use
those features for anything nontrivial. For instance, suppose we had
some list ``arr``, and we wanted to square every element of the list
and then keep only the even squares. This is how we might approach
this problem using Python's built-in functional tools. ::

    list(filter(lambda x: x % 2 == 0, map(lambda x: x ** 2, arr)))

There's a lot of cruft here, with having to explicitly declare that
we're using lambdas every time we need to make a
function. Additionally, we have to read the code almost backward to
understand what it's doing. While this backward sequencing of
operations is fine in a language like Haskell (where pointfree
notation hides the messy bracketing), in Python it would make much
more sense if we could read our code in the normal order. This is
where Alakazam comes in.

    zz.ZZ.of(arr).map(_1 ** 2).filter(_1 % 2 == 0).list()

Now the code reads left-to-right, and the lambdas are not nearly as
bulky. The ``zz.ZZ`` (which is an alias for the class
``alakazam.Alakazam``) is the entry point to any stream-based
operations you might want to perform with Alakazam. The ``of`` method
wraps any iterable in an Alakazam instance. Then the ``map`` and
``filter`` do the same thing as their global function
equivalents. Finally, the ``list`` method converts the Alakazam
iterable into an ordinary Python list. The important thing is that,
now, a cursory left-to-right reading of the code yields "arr -> map ->
filter -> list", which is the sequence of operations we're actually
performing.

The lambda syntax is also significantly shortened. In cases where your
anonymous function merely uses operators, element access, and
attribute access, you can shorten it by using the placeholder
lambdas. The placeholder constants ``_1, _2, _3, _4, _5``, based
loosely on the C++ Boost placeholders with the same names, are each
defined as callable objects which return their nth argument. If you
need more than five arguments, you can use `zz.arg(n)` directly, which
is how the placeholders are implemented in the first place. These
placeholders can be used with (almost) any built-in Python operator,
and they can also be subscripted and have arbitrary attributes
accessed on them. All of these operations will be translated into an
anonymous function that performs the corresponding operation on its
arguments. So ``_1 ** 2`` is a function that squares its first (and
only) argument, ``_1 + _2`` is a function that adds two arguments
together, and ``_1.name == "Alakazam"`` is a function which checks
whether its argument's name attribute is equal to "Alakazam".