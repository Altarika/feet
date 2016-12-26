# -*- coding: utf8 -*-
# Configuration management
#
# Author:   Romary Dupuis <romary.dupuis@altarika.com>
#
# Copyright (C) 2016 Romary Dupuis
# Licensed under the GNU LGPL v2.1 - http://www.gnu.org/licenses/lgpl.html

"""
Uses confire to get meaningful configurations from a yaml file
"""

import os
from confire import Configuration, environ_setting
from dotenv import load_dotenv

# Load Environment variables
load_dotenv(os.path.abspath('.env'))


class RedisConfiguration(Configuration):
    """
    Configuration for the Redis database
    """
    host = environ_setting('REDIS_HOST', 'localhost', required=False)
    port = int(environ_setting('REDIS_PORT', 6379, required=False))
    prefix = environ_setting('REDIS_PREFIX', 'feet', required=False)


class ServerConfiguration(Configuration):
    """
    Configuration for the web server to run an admin UI.
    """
    host = environ_setting('SERVER_HOST', 'localhost', required=False)
    port = int(environ_setting('SERVER_PORT', 8888, required=False))


class MecabConfiguration(Configuration):
    """
    Configuration for the web server to run an admin UI.
    """
    mecabdict = environ_setting(
        'MECAB_DICT',
        '/var/lib/mecab/dic/ipadic-utf8',
        required=False)


class FeetConfiguration(Configuration):
    """
    Meaningful defaults and required configurations.
    """
    CONF_PATHS = [
        "/etc/feet.yaml",  # System configuration
        os.path.expanduser("~/.feet.yaml"),  # User specific config
        os.path.abspath("conf/feet.yaml"),  # Local configuration
    ]

    debug = True
    database = RedisConfiguration()
    server = ServerConfiguration()
    mecab = MecabConfiguration()
    logfile = environ_setting('LOG_FILE', 'feet.log', required=False)
    loglevel = environ_setting('LOG_LEVEL', 'INFO', required=False)
    timeout = int(environ_setting('TIMEOUT', 180, required=False))


# Load settings immediately for import
settings = FeetConfiguration.load()


if __name__ == '__main__':
    print(settings)
