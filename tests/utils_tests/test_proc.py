# -*- coding: utf-8 -*-
# pylint: disable=misplaced-comparison-constant


"""Tests for path utils module"""


import os
import sys

import pytest

import ostrich
from ostrich.utils.proc import CalledProcessError, PIPE, run, TimeoutExpired


def test_run():
    """Test proc.run function in several timeout-less scenarios"""
    cproc = run([sys.executable, '-c', 'import sys; sys.exit(47)'])
    assert 47 == cproc.returncode
    with pytest.raises(CalledProcessError) as excinfo:
        cproc.check_returncode()
    assert 'returned non-zero exit status 47' in str(excinfo.value)

    with pytest.raises(CalledProcessError):
        run([sys.executable, '-c', 'import sys; sys.exit(47)'], check=True)

    cproc = run([sys.executable, '-c', 'import sys; sys.exit(0)'], check=True)
    assert 0 == cproc.returncode
    assert ("CompletedProcess(args=(['{0}', '-c', 'import sys; "
            "sys.exit(0)'],), returncode=0)" .format(sys.executable) ==
            repr(cproc))

    cproc = run([sys.executable, '-c', 'print("BDFL")'], stdout=PIPE)
    assert b'BDFL\n' == cproc.stdout

    cproc = run([sys.executable, '-c', 'import sys; sys.stderr.write("BDFL")'],
                stderr=PIPE)
    assert b'BDFL' == cproc.stderr

    newenv = os.environ.copy()
    newenv["FRUIT"] = "banana"
    cproc = run([sys.executable, '-c', 'import sys, os;'
                 'sys.exit(33 if os.getenv("FRUIT")=="banana" else 31)'],
                env=newenv)
    assert 33 == cproc.returncode

    cproc = run([sys.executable, '-c',
                 'import sys; sys.stdout.write(sys.stdin.read().upper())'],
                input=b'spam', stdout=PIPE)
    assert b'SPAM' == cproc.stdout

    with pytest.raises(ValueError) as excinfo:
        cproc = run([sys.executable, '-c',
                     'import sys; sys.stdout.write(sys.stdin.read().upper())'],
                    input=b'spam', stdin=PIPE, stdout=PIPE)
    assert ('stdin and input arguments may not both be used.'
            in str(excinfo.value))


def test_run_timeout():
    """Test timeout-specific proc.run scenarios

    Don't run in a timeout-less environment.
    """
    if not ostrich.utils.proc.__timeout__:
        return

    with pytest.raises(TimeoutExpired):
        run([sys.executable, '-c', 'while True: pass'], timeout=0.0001)

    with pytest.raises(TimeoutExpired) as excinfo:
        run([sys.executable, '-c',
             'import sys, time; sys.stdout.write("BDFL");'
             'sys.stdout.flush(); time.sleep(3600)'], timeout=0.1, stdout=PIPE)
    assert 'BDFL' in str(excinfo.value)
