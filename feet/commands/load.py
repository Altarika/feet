# -*- coding: utf8 -*-
# Load entities dictionary
#
# Author:   Romary Dupuis <romary.dupuis@altarika.com>
#
# Copyright (C) 2016 Romary Dupuis
# Licensed under the GNU LGPL v2.1 - http://www.gnu.org/licenses/lgpl.html

from commis import Command
from commis import color
from feet.entities.registry import Registry
from feet.entities.dictionary import CSVDictionary


class LoadCommand(Command):

    name = 'load'
    help = 'load a list of entities from a file'
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
        '--txt': {
            'metavar': 'PLAIN_FILE',
            'required': False,
            'help': 'path to a plain text file that will be loaded'
        },
        '--csv': {
            'metavar': 'CSV_FILE',
            'required': False,
            'help': 'path to a csv file that will be loaded'
        },
        '--lang': {
            'metavar': 'LANG',
            'default': 'en',
            'help': 'language of entities'
        },
        '--prefix': {
            'metavar': 'PREFIX',
            'default': 'feet',
            'help': 'prefix used for all keys of dictionary'
        }
    }

    def handle(self, args):
        """
        CLI to load an entity dictionary.
        """
        file_path = args.txt
        if args.csv is not None:
            registry = Registry.find_or_create(args.registry,
                                               dict_class=CSVDictionary,
                                               key_prefix=args.prefix)
            file_path = args.csv
        else:
            registry = Registry.find_or_create(args.registry,
                                               key_prefix=args.prefix)
            file_path = args.txt
        dictionary = registry.get_dict(args.entity)
        count = dictionary.load_file(file_path, args.lang)
        print('+ %d entities processed' % count)
        return '* %s dictionary loaded' % (color.format(args.entity,
                                                        color.GREEN))
