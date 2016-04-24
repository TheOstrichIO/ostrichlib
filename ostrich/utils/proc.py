# -*- coding: utf-8 -*-
# pylint: disable=unused-import, too-few-public-methods


"""
proc utils module

An adaptation of Python 3.5 subprocess.run function

source: https://github.com/python/cpython/blob/3.5/Lib/subprocess.py
"""


# Python 2 / Python 3 compatibility fu
# http://python-future.org/compatible_idioms.html
from __future__ import absolute_import
from __future__ import unicode_literals  # so strings without u'' are unicode

try:
    # Python 3.2 and above - use builtin subprocess module with timeout support
    import subprocess
    from subprocess import PIPE, Popen, SubprocessError, TimeoutExpired
    __timeout__ = True

except ImportError:

    try:
        # Pre-Python 3.2, try using subprocess32 package if available,
        # to gain timeout functionality
        import subprocess32 as subprocess
        from subprocess import PIPE, Popen, SubprocessError, TimeoutExpired
        __timeout__ = True

    except ImportError:
        # No subprocess32 package, gracefully degrade to no-timeout behavior

        import subprocess
        from subprocess import PIPE, Popen
        __timeout__ = False

        # Exception classes used by this module.
        class SubprocessError(Exception):
            pass

        class TimeoutExpired(SubprocessError):
            pass


class CalledProcessError(SubprocessError):
    """This exception is raised when a process run by run() with check=True
       returns a non-zero exit status.

    The exit status will be stored in the returncode attribute;
    The cmd (run args) will be stored in the cmd attribute;
    The output will be stored in output / stdout attribute;
    The stderr will be stored in stderr attribute.
    """
    def __init__(self, returncode, cmd, output=None, stderr=None):
        super(CalledProcessError, self).__init__()
        self.returncode = returncode
        self.cmd = cmd
        self.output = output
        self.stderr = stderr

    def __str__(self):
        return ("Command '{0}' returned non-zero exit status {1}"
                .format(self.cmd, self.returncode))

    @property
    def stdout(self):
        """Alias for output attribute, to match stderr"""
        return self.output


class _TimeoutExpired(TimeoutExpired):
    """This exception is raised when the timeout expires while waiting for a
       child process."""
    def __init__(self, cmd, timeout, output=None, stderr=None):
        super(_TimeoutExpired, self).__init__(cmd, timeout)
        self.cmd = cmd
        self.timeout = timeout
        self.output = output
        self.stderr = stderr

    def __str__(self):
        return ("Command '{0}' timed out after {1} seconds"
                .format(self.cmd, self.timeout))

    @property
    def stdout(self):
        return self.output


class CompletedProcess(object):
    """A process that has finished running.

    This is returned by run().

    Attributes:

    - args: The list or str args passed to run().
    - returncode: The exit code of the process, negative for signals.
    - stdout: The standard output (None if not captured).
    - stderr: The standard error (None if not captured).
    """

    def __init__(self, args, returncode, stdout=None, stderr=None):
        self.args = args
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr

    def __repr__(self):
        args = ['args={0!r}'.format(self.args),
                'returncode={0!r}'.format(self.returncode)]
        if self.stdout is not None:
            args.append('stdout={0!r}'.format(self.stdout))
        if self.stderr is not None:
            args.append('stderr={0!r}'.format(self.stderr))
        return "{0}({1})".format(type(self).__name__, ', '.join(args))

    def check_returncode(self):
        """Raise CalledProcessError if the exit code is non-zero."""
        if self.returncode:
            raise CalledProcessError(self.returncode, self.args, self.stdout,
                                     self.stderr)


def run(*popenargs, **kwargs):
    """Run command with arguments and return a `CompletedProcess` instance.

    The returned instance will have attributes args, returncode, stdout and
    stderr.

    By default, stdout and stderr are not captured, and those attributes
    will be None. Pass stdout=PIPE and/or stderr=PIPE in order to capture them.

    If `check` is True and the exit code was non-zero, it raises a
    CalledProcessError. The CalledProcessError object will have the return code
    in the returncode attribute, and output & stderr attributes if those
    streams were captured.

    If `timeout` is given, and the process takes too long, a TimeoutExpired
    exception will be raised, if timeout is supported in the underlying Popen
    implementation (e.g. Python >= 3.2, or an available subprocess32 package).

    There is an optional argument `input`, allowing you to
    pass a string to the subprocess's stdin.  If you use this argument
    you may not also use the Popen constructor's `stdin` argument, as
    it will be used internally.

    The other arguments are the same as for the Popen constructor.

    If universal_newlines=True is passed, the `input` argument must be a
    string and stdout/stderr in the returned object will be strings rather than
    bytes.
    """
    stdin = kwargs.pop('input', None)
    timeout = kwargs.pop('timeout', None)
    check = kwargs.pop('check', False)
    if stdin is not None:
        if 'stdin' in kwargs:
            raise ValueError('stdin and input arguments may not both be used.')
        kwargs['stdin'] = PIPE

    process = Popen(*popenargs, **kwargs)
    try:
        if __timeout__:
            stdout, stderr = process.communicate(stdin, timeout=timeout)
        else:
            stdout, stderr = process.communicate(stdin)
    except TimeoutExpired:
        # this will never happen if __timeout__ is False
        process.kill()
        stdout, stderr = process.communicate()
        # pylint: disable=no-member
        raise _TimeoutExpired(process.args, timeout, output=stdout,
                              stderr=stderr)
    except:
        process.kill()
        process.wait()
        raise
    retcode = process.poll()
    if check and retcode:
        raise CalledProcessError(retcode, popenargs,
                                 output=stdout, stderr=stderr)
    return CompletedProcess(popenargs, retcode, stdout, stderr)
