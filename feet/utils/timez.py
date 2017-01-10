# -*- coding: utf8 -*-
# load_dictionary
# Logging Utility for Feet
#
# Author:   Romary Dupuis <romary.dupuis@altarika.com>
# Credits: Benjamin Bengfort <benjamin@bengfort.com>

"""
Utility functions for Feet
"""

import re
import time

from dateutil.tz import tzlocal, tzutc
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


HUMAN_DATETIME = "%a %b %d %H:%M:%S %Y %z"
HUMAN_DATE = "%b %d, %Y"
HUMAN_TIME = "%I:%M:%S %p"
JSON_DATETIME = "%Y-%m-%dT%H:%M:%S.%fZ"  # Must be UTC
ISO8601_DATETIME = "%Y-%m-%dT%H:%M:%S%z"
ISO8601_DATE = "%Y-%m-%d"
ISO8601_TIME = "%H:%M:%S"
COMMON_DATETIME = "%d/%b/%Y:%H:%M:%S %z"
WEB_UTC_DATETIME = "%a, %b %d, %Y at %H:%M UTC"


def localnow():
    return datetime.now(tzlocal())


def utcnow():
    now = datetime.utcnow()
    now = now.replace(tzinfo=tzutc())
    return now


zre = re.compile(r'([\-\+]\d{4})')


def strptimez(dtstr, dtfmt):
    """
    Helper function that performs the timezone calculation to correctly
    compute the '%z' format that is not added by default in Python 2.7.
    """
    if '%z' not in dtfmt:
        return datetime.strptime(dtstr, dtfmt)

    dtfmt = dtfmt.replace('%z', '')
    offset = int(zre.search(dtstr).group(1))
    dtstr = zre.sub('', dtstr)
    delta = timedelta(hours=offset / 100)
    utctsp = datetime.strptime(dtstr, dtfmt) - delta
    return utctsp.replace(tzinfo=tzutc())


def humanizedelta(*args, **kwargs):
    """
    Wrapper around dateutil.relativedelta (same construtor args) and returns
    a humanized string representing the detla in a meaningful way.
    """
    if 'milliseconds' in kwargs:
        sec = kwargs.get('seconds', 0)
        msec = kwargs.pop('milliseconds')
        kwargs['seconds'] = sec + (float(msec) / 1000.0)

    delta = relativedelta(*args, **kwargs)
    attrs = ('years', 'months', 'days', 'hours', 'minutes', 'seconds')
    parts = [
        '%d %s' % (getattr(delta, attr),
                   getattr(delta, attr) > 1 and attr or attr[:-1])
        for attr in attrs if getattr(delta, attr)
    ]

    return " ".join(parts)


class Timer(object):
    """
    A context object timer. Usage:
        >>> with Timer() as timer:
        ...     do_something()
        >>> print timer.elapsed
    """

    def __init__(self, wall_clock=True):
        """
        If wall_clock is True then use time.time() to get the number of
        actually elapsed seconds. If wall_clock is False, use time.clock to
        get the process time instead.
        """
        self.wall_clock = wall_clock
        self.time = time.time if wall_clock else time.clock

        # Stubs for serializing an empty timer.
        self.started = None
        self.finished = None
        self.elapsed = 0.0

    def __enter__(self):
        self.started = self.time()
        return self

    def __exit__(self, typ, value, tb):
        self.finished = self.time()
        self.elapsed = self.finished - self.started

    def __str__(self):
        return humanizedelta(seconds=self.elapsed)
