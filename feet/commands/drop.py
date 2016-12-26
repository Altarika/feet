# -*- coding: utf8 -*-
# Reset entity dictionary
#
# Author:   Romary Dupuis <romary.dupuis@altarika.com>
#
# Copyright (C) 2016 Romary Dupuis
# Licensed under the GNU LGPL v2.1 - http://www.gnu.org/licenses/lgpl.html

from commis import Command
from commis import color

from feet.entities.registry import Registry


class DropCommand(Command):

    name = 'drop'
    help = 'Drop an entity dictionary'
    args = {
        '--registry': {
            'metavar': 'REGISTRY',
            'default': 'feet',
            'required': False,
            'help': 'registry of entities'
        },
        '--entity': {
            'metavar': 'ENTITY',
            'required': True,
            'help': 'entity dictionary'
        },
        '--prefix': {
            'metavar': 'PREFIX',
            'default': 'feet',
            'help': 'prefix used for all keys of dictionary'
        }
    }

    def handle(self, args):
        """
        CLI to drop an entity dictionary.
        """
        registry = Registry.find_or_create(args.registry,
                                           key_prefix=args.prefix)
        if registry.del_dict(args.entity):
            return '* %s dictionary dropped' % (color.format(args.entity,
                                                             color.GREEN))
        else:
            return '* %s unknown dictionary' % (color.format(args.entity,
                                                             color.RED))
