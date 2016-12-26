# coding: utf-8

from __future__ import unicode_literals

import logging
import sys
import yaml

try:                                                        # pragma: no cover
    from collections import UserDict                        # noqa
except ImportError:                                         # pragma: no cover
    from UserDict import UserDict                           # noqa


PY3 = sys.version_info[0] == 3

if PY3:                         # pragma: no cover
    string_types = str,         # noqa
    text_type = str             # noqa
else:                           # pragma: no cover
    string_types = basestring,  # noqa
    text_type = unicode         # noqa

log = logging.getLogger(__name__)


def yaml_load(source, loader=yaml.Loader):
    """
    Wrap PyYaml's loader so we can extend it to suit our needs.

    Load all strings as unicode.
    http://stackoverflow.com/a/2967461/3609487
    """

    def construct_yaml_str(self, node):
        """
        Override the default string handling function to always return
        unicode objects.
        """
        return self.construct_scalar(node)

    class Loader(loader):
        """
        Define a custom loader derived from the global loader to leave the
        global loader unaltered.
        """

    Loader.add_constructor('tag:yaml.org,2002:str', construct_yaml_str)

    try:
        return yaml.load(source, Loader)
    finally:
        if hasattr(source, 'close'):
            source.close()


def reduce_list(data_set):
    """ Reduce duplicate items in a list and preserve order """
    seen = set()
    return [item for item in data_set if
            item not in seen and not seen.add(item)]
