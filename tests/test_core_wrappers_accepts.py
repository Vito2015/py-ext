
import pytest
from pyextend.core.wrappers.accepts import accepts


def func_accept(f, *args, **kwargs):
    exception = TypeError if 'exception' not in kwargs else kwargs['exception']
    try:
        f(*args, **kwargs)
        return True
    except exception:
        return False


def test_accepts_single_parameter():

    def func_single_param(param_type):
        @accepts(a=param_type)
        def _func_single_param(a):
            return a
        return _func_single_param

    assert func_accept(func_single_param(int), 10) is True
    assert func_accept(func_single_param(int), []) is False
    assert func_accept(func_single_param(str), 'a') is True
    assert func_accept(func_single_param(str), 11) is False
    assert func_accept(func_single_param(list), []) is True
    assert func_accept(func_single_param(list), 'abc') is False
    assert func_accept(func_single_param(dict), {}) is True
    assert func_accept(func_single_param(dict), []) is False

    assert func_accept(func_single_param('__iter__'), 'abc') is True
    assert func_accept(func_single_param('__iter__'), (1, 2)) is True
    assert func_accept(func_single_param('__iter__'), [1, 2]) is True
    assert func_accept(func_single_param('__iter__'), {'a': 1, 'b': 2}) is True
    assert func_accept(func_single_param('__iter__'), range(10)) is True
    assert func_accept(func_single_param('__iter__'), 11) is False

    # None able parameter test
    assert func_accept(func_single_param((int, None)), None) is True
    assert func_accept(func_single_param((int, None)), 10) is True
    assert func_accept(func_single_param(('__iter__', None)), 'abc') is True
    assert func_accept(func_single_param(('__iter__', None)), None) is True


def test_accepts_multi_parameter():

    def func_multi_param(*args_types, **kwargs_types):
        kwargs_types = dict(kwargs_types, **{'arg_'+str(i): arg for i, arg in enumerate(args_types)})
        keys = sorted(kwargs_types.keys())

        def _get_params_str(**kwargs):
            params_list = [p[0]+'='+str(p[1].__name__) for p in kwargs.items() if type(p[1]).__name__ == 'type'] + \
                          [p[0]+'='+"'"+str(p[1])+"'" for p in kwargs.items() if type(p[1]).__name__ != 'type']
            return ','.join(params_list)
        # @accepts({kwargs_types})
        inner_func_str = """def func_multi_param({keys}):
    return {keys}
""".format(kwargs_types=_get_params_str(**kwargs_types), keys=','.join(keys))
        v = {}
        aaa = eval(inner_func_str, v)
        # @accepts(kwargs_types)
        # def _func_multi_param(*args):
        #     return args
        # return _func_multi_param

        return aaa

    # assert func_accept(func_multi_param(int), 10) is True
    assert func_accept(func_multi_param(int, str), 10, 'a') is True
    # assert func_accept(func_multi_param(int, str), 10, 'abc') is True
    # assert func_accept(func_single_param(int), []) is False
    # assert func_accept(func_single_param(str), 'a') is True
    # assert func_accept(func_single_param(str), 11) is False
    # assert func_accept(func_single_param(list), []) is True
    # assert func_accept(func_single_param(list), 'abc') is False
    # assert func_accept(func_single_param(dict), {}) is True
    # assert func_accept(func_single_param(dict), []) is False
    #
    # assert func_accept(func_single_param('__iter__'), 'abc') is True
    # assert func_accept(func_single_param('__iter__'), (1, 2)) is True
    # assert func_accept(func_single_param('__iter__'), [1, 2]) is True
    # assert func_accept(func_single_param('__iter__'), {'a': 1, 'b': 2}) is True
    # assert func_accept(func_single_param('__iter__'), range(10)) is True
    # assert func_accept(func_single_param('__iter__'), 11) is False
    #
    # # None able parameter test
    # assert func_accept(func_single_param((int, None)), None) is True
    # assert func_accept(func_single_param((int, None)), 10) is True
    # assert func_accept(func_single_param(('__iter__', None)), 'abc') is True
    # assert func_accept(func_single_param(('__iter__', None)), None) is True

# def test_accepts():
#         @accepts(a=int, b=('__iter__', None), c=str)
#         def test(a, b=None, c=None):
#             print('test accepts OK')
#
#         test(13, b=[], c='abc')
#
#         @accepts(a=int, b=('__iter__', None), c=str)
#         def test2(a, b=None, c=None):
#             print('test2 accepts OK')
#
#         test2(13, b=[], c='abc')
#         test2(13, b=None, c='abc')

if __name__ == '__main__':
    pytest.main(__file__)
