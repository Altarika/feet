# -*- coding: utf8 -*-
# Singleton Metaclass
#
# Author:   Romary Dupuis <romary.dupuis@altarika.com>
#
# Copyright (C) 2016 Romary Dupuis
# Licensed under the GNU LGPL v2.1 - http://www.gnu.org/licenses/lgpl.html

"""
Metaclass to easily define singleton classes
"""


class SingletonMetaClass(type):
    """
    Usage:
        class bar(object):
            __metaclass__ = SingletonMetaClass
    """
    def __init__(cls, name, bases, dict):
        super(SingletonMetaClass, cls)\
            .__init__(name, bases, dict)
        original_new = cls.__new__

        def my_new(cls, *args, **kwds):
            if cls.instance is None:
                cls.instance = original_new(cls, *args, **kwds)
            return cls.instance
        cls.instance = None
        cls.__new__ = staticmethod(my_new)
