# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import functools
import inspect

from zodiac_web.utils.helper import get_arguments


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


def inspect_required_optional_arguments(func):
    args, varargs, keywords, defaults = inspect.getargspec(func)

    if defaults:
        args_with_defaults = (dict(zip(args[-len(defaults):], defaults)))
    else:
        args_with_defaults = {}

    required_args = list(
        set(args[:]) - set(args_with_defaults.keys()) - {'self'})

    return required_args, args_with_defaults


def sequence_service(noun, verb, version=None, parameters_desc=None, description=''):
    if parameters_desc is None:
        parameters_desc = {}

    def wrap(f):

        for name, config in parameters_desc.items():
            if not {'type', 'desc'}.issuperset(config.keys()):
                raise ValueError('only %s the parameter description\'s key, '
                                 'but get %s in [%s]\'s @sequence_service descorator' %
                                 (['type', 'desc'], config.keys(), f.__name__))

        @functools.wraps(f)
        def wrapper(*args, **kwargs):

            return f(*args, **kwargs)

        required_args, optional_args = inspect_required_optional_arguments(f)

        required_args_config = collections.OrderedDict()

        for arg in required_args:
            if arg in parameters_desc:
                required_args_config[arg] = parameters_desc[arg]
            else:
                required_args_config[arg] = {
                    'type': None,
                    'desc': None
                }

        optional_args_config = collections.OrderedDict()
        for arg, default_value in optional_args.items():
            if arg in parameters_desc:
                optional_args_config[arg] = parameters_desc[arg]
            else:
                optional_args_config[arg] = {
                    'type': None,
                    'desc': None
                }

            optional_args_config[arg]['default'] = default_value

        wrapper.__service_config__ = {
            'noun': noun,
            'verb': verb,
            'version': version,
            'description': description,
            'required_args': required_args_config,
            'optional_args': optional_args_config
        }

        return wrapper

    return wrap
