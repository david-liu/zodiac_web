# -*- coding: utf-8 -*-
import inspect
from time import time
import os

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # ver. < 3.0

__all__ = ['get_arguments', 'check_function_arguments']


def how_long(func, *args):
    """Execute function with given arguments and measure execution time """
    t0 = time()
    result = func(*args)
    t1 = time()

    return result, t1 - t0


def loadConfiguration(cfg_file, section):
    """ Load a section configuration from the configuration file"""

    config = ConfigParser()
    config.read(cfg_file)

    if not config.has_section(section):
        raise ValueError('the section [%s] did not exixted in '
                         'the configuration file [%s]', section, cfg_file)

    options = config.options(section)

    propertes = {}
    for opt in options:
        propertes[opt] = config.get(section, opt)

    return propertes


def convert_to_abspath(file, path):
    if not os.path.isabs(path):
        return os.path.abspath(os.path.join(
            os.path.dirname(os.path.realpath(file)), path))

    return path


def get_arguments(func):
    """Returns list of arguments this function has."""
    if hasattr(func, '__code__'):
        # Regular function.
        return inspect.getargspec(func).args
    elif hasattr(func, '__call__'):
        # Callable object.
        print(func)
        return _get_arguments(func.__call__)
    elif hasattr(func, 'func'):
        # Partial function.
        return _get_arguments(func.func)


def inspect_required_optional_arguments(func):
    args, varargs, keywords, defaults = inspect.getargspec(func)

    if defaults:
        args_with_defaults = (dict(zip(args[-len(defaults):], defaults)))
    else:
        args_with_defaults = {}

    required_args = list(
        set(args[:]) - set(args_with_defaults.keys()) - set(['self']))

    return required_args, args_with_defaults


def check_function_arguments(fn, allowed_arguments, required_arguments=None):
    arguments = set(get_arguments(fn))

    if not set(allowed_arguments).issuperset(arguments):
        raise ValueError('The parameters of function should be in '
                         '[%s], Got %s(%s)' %
                         (','.join(allowed_arguments),
                          fn.__name__,
                          ', '.join(arguments)))

    if (required_arguments is not None) and (not arguments.issuperset(set(required_arguments))):
        raise ValueError('The parameters [%s] is required by the function, '
                         'Got %s(%s)' % (','.join(required_arguments), fn.__name__,
                                         ', '.join(arguments)))
