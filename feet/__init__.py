#!/usr/bin/env python
# coding: utf-8

# __init__ for feet library
#
# Author:   Romary Dupuis <romary.dupuis@altarika.com>
#
# Copyright (C) 2016 Romary Dupuis
# Licensed under the GNU LGPL v2.1 - http://www.gnu.org/licenses/lgpl.html

"""
Implements the Feet console app.
"""

from feet.entities.dictionary import Dictionary
from feet.entities.extractor import Extractor
from .__main__ import COMMANDS
from .__main__ import FeetApp


__all__ = ['Dictionary', 'Extractor']
