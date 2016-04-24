# -*- coding: utf-8 -*-
# pylint: disable=misplaced-comparison-constant


"""Tests for path utils module"""


import pytest

from ostrich.utils.path import commonpath, nt_commonpath, posix_commonpath


def test_posix_commonpath_abs():
    """Test POSIX-specific commonpath with absolute paths."""
    assert '/usr/local' == posix_commonpath(['/usr/local'])
    assert '/usr/local' == posix_commonpath(['/usr/local', '/usr/local'])
    assert b'/usr/local' == posix_commonpath([b'/usr/local', b'/usr/local/'])
    assert u'/usr/local' == posix_commonpath([u'//usr/local', u'/usr//local'])
    assert '/usr/local' == posix_commonpath(['/./usr/local', '/usr/./local'])
    assert '/' == posix_commonpath(['/', '/dev'])
    assert '/' == posix_commonpath(['/usr', '/dev'])
    assert '/usr/lib' == posix_commonpath(['/usr/lib/', '/usr/lib/python3'])
    # Actually check the difference from commonprefix
    assert '/usr' == posix_commonpath(['/usr/lib/', '/usr/lib64/'])
    assert '/usr' == posix_commonpath(['/usr/lib', '/usr/lib64'])
    assert '/usr' == posix_commonpath(['/usr/lib/', '/usr/lib64'])


def test_posix_commonpath_rel():
    """Test POSIX-specific commonpath with relative paths."""
    assert 'spam' == posix_commonpath(['spam'])
    assert 'spam' == posix_commonpath(['spam', 'spam'])
    assert '' == posix_commonpath(['spam', 'alot'])
    assert 'and' == posix_commonpath(['and/spam', 'and/jam'])
    assert 'and' == posix_commonpath(['and//spam', 'and/jam//'])
    assert 'and' == posix_commonpath(['and/./spam', './and/jam//'])
    assert '' == posix_commonpath(['and/spam', 'and/jam', 'alot'])
    assert 'and' == posix_commonpath(['and/spam', 'and/jam', 'and'])
    assert '' == posix_commonpath([''])
    assert '' == posix_commonpath(['', 'spam/alot'])
    # Actually check the difference from commonprefix
    assert 'i' == posix_commonpath(['i/spam/a/lot', 'i/spa/m/alot'])


def test_posix_commonpath_err():
    """Test POSIX-specific commonpath in error conditions."""
    for bad_paths in (
            ['/usr', 'usr'],
            ['usr', '/usr'],
            [],
    ):
        with pytest.raises(ValueError):
            posix_commonpath(bad_paths)
    with pytest.raises(TypeError):
        posix_commonpath([b'/usr/lib/', u'/usr/lib/python3'])
    with pytest.raises(TypeError):
        posix_commonpath([u'/usr/lib/', b'/usr/lib/python3'])


def test_nt_commonpath_abs():
    """Test NT-specific commonpath with absolute paths."""
    assert 'C:\\Program Files' == nt_commonpath(['C:\\Program Files'])
    assert ('C:\\Program Files' ==
            nt_commonpath(['C:\\Program Files', 'C:\\Program Files']))
    assert ('C:\\Program Files' ==
            nt_commonpath(['C:\\Program Files\\', 'C:\\Program Files']))
    assert ('C:\\Program Files' ==
            nt_commonpath(['C:\\Program Files\\', 'C:\\Program Files\\']))
    assert ('C:\\Program Files' ==
            nt_commonpath(['C:\\\\Program Files', 'C:\\Program Files\\\\']))
    assert ('C:\\Program Files' ==
            nt_commonpath(['C:\\.\\Program Files', 'C:\\Program Files\\.']))
    assert 'C:\\' == nt_commonpath(['C:\\', 'C:\\bin'])
    assert 'C:\\' == nt_commonpath(['C:\\Program Files', 'C:\\bin'])
    assert ('C:\\Program Files' ==
            nt_commonpath(['C:\\Program Files', 'C:\\Program Files\\Bar']))
    assert ('C:\\Program Files' ==
            nt_commonpath(['C:\\Program Files\\Foo',
                           'C:\\Program Files\\Bar']))
    assert 'C:\\' == nt_commonpath(['C:\\Program Files', 'C:\\Projects'])
    assert 'C:\\' == nt_commonpath(['C:\\Program Files\\', 'C:\\Projects'])
    assert ('C:\\Program Files' ==
            nt_commonpath(['C:\\Program Files\\Foo', 'C:/Program Files/Bar']))
    assert ('C:\\Program Files' ==
            nt_commonpath(['C:\\Program Files\\Foo', 'c:/program files/bar']))
    assert ('c:\\program files' ==
            nt_commonpath(['c:/program files/bar', 'C:\\Program Files\\Foo']))


def test_nt_commonpath_rel():
    """Test NT-specific commonpath with relative paths."""
    assert 'spam' == nt_commonpath(['spam'])
    assert 'spam' == nt_commonpath(['spam', 'spam'])
    assert '' == nt_commonpath(['spam', 'alot'])
    assert b'and' == nt_commonpath([b'and\\spam', b'and\\jam'])
    assert u'and' == nt_commonpath([u'and\\\\spam', u'and\\jam\\\\'])
    assert 'and' == nt_commonpath(['and\\.\\spam', '.\\and\\jam\\\\'])
    assert 'and' == nt_commonpath(['and\\.\\spam', '.\\and\\jam\\\\'])
    assert 'C:and' == nt_commonpath(['C:and\\spam', 'C:and\\jam', 'C:and'])
    assert 'and' == nt_commonpath(['and\\spam', 'and/jam', 'and'])
    assert '' == nt_commonpath([''])
    assert '' == nt_commonpath(['', 'spam/alot'])
    # Actually check the difference from commonprefix
    assert 'i' == nt_commonpath(['i\\spam\\a\\lot', 'i/spa/m/alot'])


def test_nt_commonpath_err():
    """Test NT-specific commonpath in error conditions."""
    for bad_paths in (
            ['C:\\Program Files', 'Program Files'],
            ['C:\\Program Files', 'C:Program Files'],
            ['\\Program Files', 'Program Files'],
            ['Program Files', 'C:\\Program Files'],
            ['C:\\Program Files', 'D:\\Program Files'],  # not same drive
            ['', '\\spam\\alot'],
            [],
    ):
        with pytest.raises(ValueError):
            nt_commonpath(bad_paths)
    with pytest.raises(TypeError):
        nt_commonpath([b'C:\\Program Files', u'C:\\Program Files\\Foo'])
    with pytest.raises(TypeError):
        nt_commonpath([u'C:\\Program Files', b'C:\\Program Files\\Foo'])


def test_generic_commonpath():
    assert 'foo' == commonpath(['foo/bar', 'foo/baz'])


def test_generic_commonpath_err():
    with pytest.raises(TypeError):
        commonpath([None])
