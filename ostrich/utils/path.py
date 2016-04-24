# -*- coding: utf-8 -*-
# pylint: disable=redefined-builtin, redefined-variable-type


"""
path utils module
"""


# Python 2 / Python 3 compatibility fu
# http://python-future.org/compatible_idioms.html
from __future__ import absolute_import
from __future__ import unicode_literals  # so strings without u'' are unicode

# uniform unicode type across Python's
from builtins import bytes, str  # from "future" library

import os


def check_arg_types(funcname, *args):
    """Raise TypeError if not all items of `args` are same string type."""
    hasstr = hasbytes = False
    for arg in args:
        if isinstance(arg, str):
            hasstr = True
        elif isinstance(arg, bytes):
            hasbytes = True
        else:
            raise TypeError('{0}() argument must be str or bytes, not {1}'
                            .format(funcname, arg.__class__.__name__))
    if hasstr and hasbytes:
        raise TypeError("Can't mix strings and bytes in path components")


def posix_commonpath(paths):
    """Given a sequence of POSIX path names,
       return the longest common sub-path."""

    if not paths:
        raise ValueError('commonpath() arg is an empty sequence')

    check_arg_types('commonpath', *paths)

    if isinstance(paths[0], bytes):
        sep = b'/'
        curdir = b'.'
    else:
        sep = '/'
        curdir = '.'

    split_paths = [path.split(sep) for path in paths]

    try:
        isabs, = set(p[:1] == sep for p in paths)
    except ValueError:
        raise ValueError("Can't mix absolute and relative paths")

    split_paths = [[c for c in s if c and c != curdir] for s in split_paths]
    s_min = min(split_paths)
    s_max = max(split_paths)
    common = s_min
    for i, run_c in enumerate(s_min):
        if run_c != s_max[i]:
            common = s_min[:i]
            break

    prefix = sep if isabs else sep[:0]
    return prefix + sep.join(common)


def nt_commonpath(paths):  # pylint: disable=too-many-locals
    """Given a sequence of NT path names,
       return the longest common sub-path."""

    from ntpath import splitdrive

    if not paths:
        raise ValueError('commonpath() arg is an empty sequence')

    check_arg_types('commonpath', *paths)

    if isinstance(paths[0], bytes):
        sep = b'\\'
        altsep = b'/'
        curdir = b'.'
    else:
        sep = '\\'
        altsep = '/'
        curdir = '.'

    drivesplits = [splitdrive(p.replace(altsep, sep).lower()) for p in paths]
    split_paths = [p.split(sep) for d, p in drivesplits]

    try:
        isabs, = set(p[:1] == sep for d, p in drivesplits)
    except ValueError:
        raise ValueError("Can't mix absolute and relative paths")

    # Check that all drive letters or UNC paths match. The check is made
    # only now otherwise type errors for mixing strings and bytes would not
    # be caught.
    if len(set(d for d, p in drivesplits)) != 1:
        raise ValueError("Paths don't have the same drive")

    drive, path = splitdrive(paths[0].replace(altsep, sep))
    common = path.split(sep)
    common = [c for c in common if c and c != curdir]

    split_paths = [[c for c in s if c and c != curdir] for s in split_paths]
    s_min = min(split_paths)
    s_max = max(split_paths)
    for i, run_c in enumerate(s_min):
        if run_c != s_max[i]:
            common = common[:i]
            break
    else:
        common = common[:len(s_min)]

    prefix = drive + sep if isabs else drive
    return prefix + sep.join(common)


def commonpath(paths):
    """Return the longest common sub-path of each pathname in paths sequence.

    Raise ValueError if paths contains both absolute and relative pathnames,
    or if paths is empty.

    Unlike :py:func:`os.path.commonprefix()`, this returns a valid path:

    >>> print(commonpath(['foo/bar', 'foo/baz', 'foo/baaam']))
    foo
    >>> from os.path import commonprefix
    >>> print(commonprefix(['foo/bar', 'foo/baz', 'foo/baaam']))
    foo/ba

    Adapted from the source code of Python 3.5.1.
    """
    if os.name == 'posix':
        return posix_commonpath(paths)
    return nt_commonpath(paths)
