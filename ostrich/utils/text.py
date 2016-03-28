# -*- coding: utf-8 -*-


"""
text utils module

A collection of text-related utility functions. Hurray!
"""


# Python 2 / Python 3 compatibility fu
# http://python-future.org/compatible_idioms.html
from __future__ import absolute_import
from __future__ import unicode_literals  # so strings without u'' are unicode

# uniform unicode type across Python's
from builtins import str as text  # from "future" library

import re
import unicodedata


_SAFE_PATH_RE = re.compile(r'[^a-zA-Z0-9\-\_\=\.]')
_MAX_PATH_NAME_LEN = 255


def as_text(str_or_bytes, encoding='utf-8', errors='strict'):
    """Return input string as a text string.

    Should work for input string that's unicode or bytes,
    given proper encoding.

    >>> print(as_text(b'foo'))
    foo
    >>> b'foo'.decode('utf-8') == u'foo'
    True
    """
    if isinstance(str_or_bytes, text):
        return str_or_bytes
    return str_or_bytes.decode(encoding, errors)


def get_safe_path(in_str):
    """Return `in_str` converted to a string that can be be safely used as a
       path (either filename, or directory name).

    >>> print(get_safe_path("hello world, what's up?.txt"))
    hello_world__what_s_up_.txt

    Surrounding spaces are removed, and other "bad characters"
    are replaced with an underscore.
    The function attempts to replace unicode symbols (outside ASCII range)
    with ASCII equivalents (NFKD normalization).
    Everything else is also replaced with underscore.

    :warning: The function just returns a safe string to be used as a path.
              It DOES NOT promise anything about the existence or uniqueness
              of the path in the filesystem! Because of the conversions, many
              input strings will result the same output string, so it is the
              responsibility of the caller to decide how to handle this!

    >>> get_safe_path(' foo/bar.baz') == get_safe_path('foo$bar.baz ')
    True
    """
    norm_str = _SAFE_PATH_RE.sub(
        '_', unicodedata.normalize('NFKD', as_text(in_str)).strip())
    if len(norm_str.strip('.')) == 0:
        # making sure the normalized result is non-empty, and not just dots
        raise ValueError(in_str)
    return norm_str[:_MAX_PATH_NAME_LEN]
