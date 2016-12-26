#!/usr/bin/env python
# coding: utf-8

# __main__ for feet command
#
# Author:   Romary Dupuis <romary.dupuis@altarika.com>
#
# Copyright (C) 2016 Romary Dupuis
# Licensed under the GNU LGPL v2.1 - http://www.gnu.org/licenses/lgpl.html

"""
Definition of the Feet app and commands
"""

import logging
from commis import color
from commis import ConsoleProgram

from feet.version import __version__
from feet.commands.run import RunCommand
from feet.commands.load import LoadCommand
from feet.commands.drop import DropCommand
from feet.commands.extract import ExtractCommand
log = logging.getLogger(__name__)

DESCRIPTION = "Management and administration commands for Feet"
EPILOG = "If there are any bugs or concerns, submit an issue on Bitbucket"
COMMANDS = (
    RunCommand,
    LoadCommand,
    DropCommand,
    ExtractCommand
)


class FeetApp(ConsoleProgram):
    """
    Feet CLI app
    """
    description = color.format(DESCRIPTION, color.CYAN)
    epilog = color.format(EPILOG, color.MAGENTA)
    version = color.format("feet v{}", color.CYAN, __version__)

    @classmethod
    def load(klass, commands=COMMANDS):
        utility = klass()
        for command in commands:
            utility.register(command)
        return utility


def cli():
    app = FeetApp.load()
    app.execute()


if __name__ == '__main__':  # pragma: no cover
    cli()
