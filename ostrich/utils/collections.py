# -*- coding: utf-8 -*-


"""
collections utils module

A bunch of collections-related utility functions. Hazza!
"""

# Python 2 / Python 3 compatibility fu
# http://python-future.org/compatible_idioms.html
from __future__ import absolute_import
from __future__ import unicode_literals  # so strings without u'' are unicode

from types import GeneratorType

# no more xrange for the generator one across Python's,
# thanks to the "future" library
from builtins import range  # pylint: disable=redefined-builtin
import past.builtins


def listify(args):
    """Return args as a list.

    If already a list - return as is.

    >>> listify([1, 2, 3])
    [1, 2, 3]

    If a set - return as a list.

    >>> listify(set([1, 2, 3]))
    [1, 2, 3]

    If a tuple - return as a list.

    >>> listify(tuple([1, 2, 3]))
    [1, 2, 3]

    If a generator (also range / xrange) - return as a list.

    >>> listify(x + 1 for x in range(3))
    [1, 2, 3]
    >>> from past.builtins import xrange
    >>> from builtins import range
    >>> listify(xrange(1, 4))
    [1, 2, 3]
    >>> listify(range(1, 4))
    [1, 2, 3]

    If a single instance of something that isn't any of the above - put as a
    single element of the returned list.

    >>> listify(1)
    [1]

    If "empty" (None or False or '' or anything else that evaluates to False),
    return an empty list ([]).

    >>> listify(None)
    []
    >>> listify(False)
    []
    >>> listify('')
    []
    >>> listify(0)
    []
    >>> listify([])
    []
    """
    if args:
        if isinstance(args, list):
            return args
        elif isinstance(args, (set, tuple, GeneratorType,
                               range, past.builtins.xrange)):
            return list(args)
        return [args]
    return []
