# coding: utf-8
"""
    py_ext.core.wrappers
    ~~~~~~~~~~~~~~~~~~~~
    py_ext core wrappers packages

    :copyright: (c) 2016 by Vito.
    :license: GNU, see LICENSE for more details.
"""

from .singleton import singleton
from .accepts import accepts
from .timethis import timethis

__all__ = ['singleton', 'accepts', 'timethis']

import py_ext.core.log as log

log.set_logger(name='py_ext.core.wrappers', with_filehandler=False)
