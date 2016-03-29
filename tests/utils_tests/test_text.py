# -*- coding: utf-8 -*-
# pylint: disable=misplaced-comparison-constant


"""Tests for text utils module"""


from __future__ import unicode_literals

import pytest

from ostrich.utils.text import get_safe_path


def test_safe_path_spaces():
    """Check that surrounding spaces are removed,
       and internal spaces are converted to _"""
    assert 'foo_bar' == get_safe_path(' foo bar ')


def test_safe_path_chars():
    """Check that some chars are converted to _ and some are preserved"""
    assert ('foo_1-=___________________________' ==
            get_safe_path('foo_1-=!@#$%^&*()+[]{}<>/\\?,"\';:`~'))


def test_safe_path_unicode():
    """Check that unicode is normalized (NFKD), or converted to _"""
    assert ('foo1_b_a-r_baz_m.o=o_o______' ==
            get_safe_path('foo1/b_a-r:baz@m.o=o \u00f6 עוגי'))


def test_safe_path_bytes():
    assert 'foo.bar' == get_safe_path(b'foo.bar')


def test_safe_path_no_traversal():
    assert '.._.._.._etc_passwd' == get_safe_path('../../../etc/passwd')


def test_safe_path_empty_err():
    with pytest.raises(ValueError):
        get_safe_path('')


def test_safe_path_only_dot_err():
    with pytest.raises(ValueError):
        get_safe_path('..')


def test_safe_path_too_long():
    """Check that a long path name is trimmed to 255 characters"""
    assert 255 == len(get_safe_path(''.join('a' for _ in range(5000))))
