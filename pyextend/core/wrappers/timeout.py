# coding: utf-8
"""
    pyextend.core.wrappers.timeout
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    pyextend core wrappers timeout wrapper

    :copyright: (c) 2016 by Vito.
    :license: GNU, see LICENSE for more details.
"""
import signal
import functools
from . import system as sys

# class TimeoutError(Exception): pass


def timeout(seconds, error_message=None):
    """Timeout checking just for Linux-like platform, not working in Windows platform."""
    def decorated(func):
        result = ""

        def _handle_timeout(signum, frame):
            errmsg = error_message or 'TimeoutError: the action <%s> is timeout, %s seconds!' % (func.__name__, seconds)

            global result
            result = errmsg
            raise TimeoutError(errmsg)

        @sys.platform(sys.UNIX_LIKE, case_false_wraps=func)
        def wrapper(*args, **kwargs):
            global result
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)

            # change to also raise TimeoutError
            # try:
            #     result = func(*args, **kwargs)
            # finally:
            #     signal.alarm(0)
            #     return result
            try:
                result = func(*args, **kwargs)
            except TimeoutError as e:
                raise e
            finally:
                signal.alarm(0)
                return result
        return functools.wraps(func)(wrapper)

    return decorated
