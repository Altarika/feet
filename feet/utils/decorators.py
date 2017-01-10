# -*- coding: utf8 -*-
# load_dictionary
# Logging Utility for Feet
# Credits: Benjamin Bengfort <benjamin@bengfort.com>

"""
Decorators and function utilities for feet.
"""


import signal
from functools import wraps
from feet.utils.timez import Timer
from feet.exceptions import FeetError, TimeoutError


def memoized(fget):
    """
    Return a property attribute for new-style classes that only calls its
    getter on the first access. The result is stored and on subsequent
    accesses is returned, preventing the need to call the getter any more.
    https://github.com/estebistec/python-memoized-property
    """
    attr_name = '_{0}'.format(fget.__name__)

    @wraps(fget)
    def fget_memoized(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fget(self))
        return getattr(self, attr_name)

    return property(fget_memoized)


def timeit(func):
    """
    Returns the number of seconds that a function took along with the result
    """

    @wraps(func)
    def timer_wrapper(*args, **kwargs):
        """
        Inner function that uses the Timer context object
        """
        with Timer() as timer:
            result = func(*args, **kwargs)

        return result, timer

    return timer_wrapper


def timeout(seconds):
    """
    Raises a TimeoutError if a function does not terminate within
    specified seconds.
    """
    def _timeout_error(signal, frame):
        raise TimeoutError("Operation did not finish within \
        {} seconds".format(seconds))

    def timeout_decorator(func):

        @wraps(func)
        def timeout_wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _timeout_error)
            signal.alarm(seconds)
            try:
                return func(*args, **kwargs)
            finally:
                signal.alarm(0)

        return timeout_wrapper

    return timeout_decorator


def reraise(klass=FeetError, message=None, trap=Exception):
    """
    Catches exceptions (those specified by trap) and then reraises the
    exception type specified by class. Also embeds the original exception as
    a property of the new exception: `error.original`. Finally you can
    specify another message to raise, otherwise the error string is used.
    """

    def reraise_decorator(func):

        @wraps(func)
        def reraise_wrapper(*args, **kwargs):
            """
            Capture Wrapper
            """
            try:
                return func(*args, **kwargs)
            except trap as e:
                error = klass(message or e.message)
                error.original = e
                raise error

        return reraise_wrapper

    return reraise_decorator
