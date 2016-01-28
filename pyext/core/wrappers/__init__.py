# coding: utf-8
"""
    pyext.core.wrappers
    ~~~~~~~~~~~~~~~~~~~~
    pyext core wrappers packages

    :copyright: (c) 2016 by Vito.
    :license: GNU, see LICENSE for more details.
"""

from .singleton import singleton
from .accepts import accepts
from .timethis import timethis

__all__ = ['singleton', 'accepts', 'timethis']
