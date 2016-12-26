# -*- coding: utf8 -*-
# Launch feet server
#
# Author:   Romary Dupuis <romary.dupuis@altarika.com>
#
# Copyright (C) 2016 Romary Dupuis
# Licensed under the GNU LGPL v2.1 - http://www.gnu.org/licenses/lgpl.html

from commis import Command
from feet.config import settings
from feet.www.app import run


class RunCommand(Command):

    name = 'run'
    help = 'run the feet server application'
    args = {
        '--host': {
            'metavar': 'ADDR',
            'default': settings.server.host,
            'help': 'set the host to run the app on'
        },
        '--port': {
            'metavar': 'PORT',
            'type': int,
            'default': settings.server.port,
            'help': 'set the port to run the app on'
        },
        '--debug': {
            'action': 'store_true',
            'required': False,
            'help': 'force debug mode'
        }
    }

    def handle(self, args):
        """
        CLI to run the Feet HTTP API server application.
        """
        kwargs = {
            'host': args.host,
            'port': args.port,
            'debug': args.debug or settings.debug,
        }

        run(**kwargs)
        return " * Web application stopped"
