# coding: utf-8
"""
    py-ext.core.wrappers
    ~~~~~~~~~~~~~~~~~~~~
    py-ext core wrappers packages

    :copyright: (c) 2016 by Vito.
    :license: GNU, see LICENSE for more details.
"""

from .singleton import singleton
from .accepts import accepts
from .timethis import timethis

__all__ = ['singleton', 'accepts', 'timethis']

import core.log as log

log.set_logger(name='py-ext.core.wrappers', with_filehandler=False)
