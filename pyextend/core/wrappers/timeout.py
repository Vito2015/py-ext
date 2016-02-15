# coding: utf-8
"""
    pyextend.core.wrappers.timeout
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    pyextend core wrappers timeout wrapper

    :copyright: (c) 2016 by Vito.
    :license: GNU, see LICENSE for more details.
"""
import signal, functools


# class TimeoutError(Exception): pass


def timeout(seconds, error_message="Timeout Error: the command 30s have not finished."):
    def decorated(func):
        result = ""

        def _handle_timeout(signum, frame):
            global result
            result = error_message
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            global result
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            signal.getsignal()
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
                return result
        return functools.wraps(func)(wrapper)
    return decorated
