# -*- coding: utf8 -*-
# urls
#
# Author:   Romary Dupuis <romary.dupuis@altarika.com>
#
# Copyright (C) 2016 Romary Dupuis
# Licensed under the GNU LGPL v2.1 - http://www.gnu.org/licenses/lgpl.html

"""
TornadoWeb application definition in Feet.
"""
from tornado.web import url, Application
from feet.www.handlers.main_handler import MainHandler
from feet.www.handlers.entities import (RegistriesHandler,
                                        RegistryHandler, EntityHandler,
                                        LanguageHandler,
                                        ExtractHandler,
                                        TermsHandler, TermHandler)

RESOURCE_DATABASE = 'database'
RESOURCE_PREFIX = 'prefix'
RESOURCE_REGISTRY = 'registries'
RESOURCE_ENTITY = 'entities'
RESOURCE_LANGUAGE = 'lang'
RESOURCE_TERM = 'terms'
RESOURCE_EXTRACT = 'extract'


def handlers():
    return [
        url(r'^/$', MainHandler),
        url(r'^/{}/(\w+)/{}/(\w+)/{}/$'
            .format(RESOURCE_DATABASE, RESOURCE_PREFIX, RESOURCE_REGISTRY),
            RegistriesHandler, name='registries'),
        url(r'^/{}/(\w+)/{}/(\w+)/{}/(\w+)/$'
            .format(RESOURCE_DATABASE, RESOURCE_PREFIX, RESOURCE_REGISTRY),
            RegistryHandler, name='registry'),
        url(r'^/{}/(\w+)/{}/(\w+)/{}/(\w+)/{}/(\w+)/$'
            .format(RESOURCE_DATABASE, RESOURCE_PREFIX, RESOURCE_REGISTRY,
                    RESOURCE_ENTITY),
            EntityHandler, name='entity'),
        url(r'^/{}/(\w+)/{}/(\w+)/{}/(\w+)/{}/(\w+)/{}/(\w+)/$'
            .format(RESOURCE_DATABASE, RESOURCE_PREFIX, RESOURCE_REGISTRY,
                    RESOURCE_ENTITY, RESOURCE_LANGUAGE),
            LanguageHandler, name='language'),
        url(r'^/{}/(\w+)/{}/(\w+)/{}/(\w+)/{}/(\w+)/{}/(\w+)/{}/$'
            .format(RESOURCE_DATABASE, RESOURCE_PREFIX, RESOURCE_REGISTRY,
                    RESOURCE_ENTITY, RESOURCE_LANGUAGE, RESOURCE_TERM),
            TermsHandler, name='terms'),
        url(r'^/{}/(\w+)/{}/(\w+)/{}/(\w+)/{}/(\w+)/{}/(\w+)/{}/(\w+)/$'
            .format(RESOURCE_DATABASE, RESOURCE_PREFIX, RESOURCE_REGISTRY,
                    RESOURCE_ENTITY, RESOURCE_LANGUAGE, RESOURCE_TERM),
            TermHandler, name='term'),
        url(r'^/{}/(\w+)/{}/(\w+)/{}/(\w+)/{}/(\w+)/{}/(\w+)/{}/$'
            .format(RESOURCE_DATABASE, RESOURCE_PREFIX, RESOURCE_REGISTRY,
                    RESOURCE_ENTITY, RESOURCE_LANGUAGE, RESOURCE_EXTRACT),
            ExtractHandler, name='extract_entity')
    ]


def make_app():
    return Application(handlers())
