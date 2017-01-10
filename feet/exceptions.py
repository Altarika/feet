# -*- coding: utf8 -*-
# Exceptions
#
# Author:   Romary Dupuis <romary.dupuis@altarika.com>
#
# Copyright (C) 2016 Romary Dupuis
# Licensed under the GNU LGPL v2.1 - http://www.gnu.org/licenses/lgpl.html

from __future__ import unicode_literals


class FeetError(Exception):
    """The root of all errors in Feet library"""
    pass


class FeetCmdError(FeetError):
    """Base exceptions for all Feet command Exceptions"""
    pass


class ConfigurationError(FeetCmdError):
    """Error in configuration of Feet command"""
    pass


class TimeoutError(Exception):
    """
    An operation timed out
    """
    pass
