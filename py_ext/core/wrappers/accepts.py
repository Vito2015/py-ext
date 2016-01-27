# coding: utf-8
"""
    py_ext.core.wrappers.accepts
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    py_ext core wrappers accepts wrapper

    :copyright: (c) 2016 by Vito.
    :license: GNU, see LICENSE for more details.
"""

import functools


def accepts(exception=ValueError, **types):
    """函数参数类型检查"""

    def check_accepts(f):
        assert len(types) == f.__code__.co_argcount,\
            'accept number of arguments not equal with function number of arguments in "{}"'.format(f.__name__)

        @functools.wraps(f)
        def new_f(*args, **kwargs):
            for i, v in enumerate(args):
                if f.__code__.co_varnames[i] in types and \
                        not isinstance(v, types[f.__code__.co_varnames[i]]):
                    raise exception("function '%s' arg '%s'=%r does not match %s" %
                                    (f.__name__, f.__code__.co_varnames[i], v, types[f.__code__.co_varnames[i]]))
                    del types[f.__code__.co_varnames[i]]

            for k, v in kwargs.items():
                if k in types and not isinstance(v, types[k]):
                    raise exception("function '%s' arg '%s'=%r does not match %s" % (f.__name__, k, v, types[k]))
            return f(*args, **kwargs)
        return new_f
    return check_accepts


if __name__ == '__main__':
    def test_accepts():
        @accepts(a=int, b=list, c=str)
        def test(a, b=None, c=None):
            print('accepts OK')

        test(13, b=[], c='abc')

    test_accepts()
