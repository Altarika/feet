# -*- coding: utf8 -*-
# Extract entities from text
#
# Author:   Romary Dupuis <romary.dupuis@altarika.com>
#
# Copyright (C) 2016 Romary Dupuis
# Licensed under the GNU LGPL v2.1 - http://www.gnu.org/licenses/lgpl.html

from commis import Command
from commis import color

from feet.entities.extractor import Extractor
from feet.entities.registry import Registry


class ExtractCommand(Command):

    name = 'extract'
    help = 'extract a list of entities from text'
    args = {
        '--text': {
            'metavar': 'TEXT',
            'required': False,
            'help': 'plain text'
        },
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
        '--grammar': {
            'metavar': 'GRAMMAR',
            'required': False,
            'help': 'grammar that defines entities in a sentence'
        },
        '--path': {
            'metavar': 'PATH',
            'required': False,
            'help': 'path to the file that will be processed'
        },
        '--lang': {
            'metavar': 'LANG',
            'default': 'en',
            'help': 'language of text: en, ja, fr etc.'
        },
        '--prefix': {
            'metavar': 'PREFIX',
            'default': 'feet',
            'help': 'prefix used for all keys of entity'
        }
    }

    def handle(self, args):
        """
        CLI to extract entities from text.
        """
        if args.text is None and args.path is None:
            return color.format('* no text source specified', color.RED)
        registry = Registry.find_or_create(args.registry,
                                           key_prefix=args.prefix)
        entity = registry.get_dict(args.entity)
        engine = Extractor(entity, args.grammar)
        if args.path is not None:
            text = open(args.path).read()
        else:
            text = args.text
        results = engine.extract(text, args.lang)
        entities = []
        for element in results[0]:
            if element['entity_found'] == 1:
                entities = list(set(entities).union(
                    element['entity_candidates']))
        if len(entities) > 0:
            print(color.format('%d entities detected' % len(entities),
                               color.GREEN))
            print('\n'.join(entities))
        else:
            print(color.format('no entities detected', color.RED))
        # print(color.format('%d' % results[1].elapsed, color.LIGHT_MAGENTA))
        return '* text processed according to %s entity' %\
            (color.format(args.entity, color.GREEN))
