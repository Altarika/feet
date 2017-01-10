# -*- coding: utf8 -*-
# entities endpoint
#
# Author:   Romary Dupuis <romary.dupuis@altarika.com>
#
# Copyright (C) 2016 Romary Dupuis
# Licensed under the GNU LGPL v2.1 - http://www.gnu.org/licenses/lgpl.html

import traceback
from tornado.web import RequestHandler, MissingArgumentError
from tornado.escape import json_decode, json_encode
from feet.entities.extractor import Extractor
from feet.entities.registry import Registry
from feet.utils.logger import LoggingMixin


class RegistriesHandler(LoggingMixin, RequestHandler):
    """
    Handler to get the list of registries in the system
    """
    def get(self, database, prefix):
        try:
            registries = Registry.list(key_prefix=prefix,
                                       redis_db=int(database))
            self.write(json_encode({'registries': registries}))
        except MissingArgumentError:
            raise
        except Exception:
            self.logger.error(traceback.format_exc())
            self.send_error(500)


class RegistryHandler(LoggingMixin, RequestHandler):
    """
    Handler for the management of a registry resource
    Allows to get, add and delete registries
    """
    def get(self, database, prefix, registry):
        try:
            if registry not in Registry.list(key_prefix=prefix,
                                             redis_db=int(database)):
                return self.send_error(400)
            reg = Registry.find_or_create(registry,
                                          key_prefix=prefix,
                                          redis_db=int(database))
            self.write(json_encode({'entities': reg.dictionaries()}))
        except MissingArgumentError:
            raise
        except Exception:
            self.logger.error(traceback.format_exc())
            self.send_error(500)

    def post(self, database, prefix, registry):
        try:
            # TODO: Check size and format of registry name
            Registry.find_or_create(registry,
                                    key_prefix=prefix,
                                    redis_db=int(database))
        except MissingArgumentError:
            raise
        except Exception:
            self.logger.error(traceback.format_exc())
            self.send_error(500)

    def delete(self, database, prefix, registry):
        try:
            reg = Registry.find_or_create(registry,
                                          key_prefix=prefix,
                                          redis_db=int(database))
            reg.delete()
        except MissingArgumentError:
            raise
        except Exception:
            self.logger.error(traceback.format_exc())
            self.send_error(500)


class EntityHandler(LoggingMixin, RequestHandler):
    """
    Handler for entity endpoint
    Provides information about the entity: list of languages supported
    Allows to get, add and delete languages
    """
    def get(self, database, prefix, registry, dictionary):
        try:
            reg = Registry.find_or_create(registry,
                                          key_prefix=prefix,
                                          redis_db=int(database))
            if dictionary not in reg.dictionaries():
                return self.send_error(400)
            entity = reg.get_dict(dictionary)
            self.write(json_encode(
                {'languages': entity.languages()}))
        except MissingArgumentError:
            raise
        except Exception:
            self.logger.error(traceback.format_exc())
            self.send_error(500)

    def post(self, database, prefix, registry, dictionary):
        try:
            # TODO: Check size and format of entity name
            reg = Registry.find_or_create(registry,
                                          key_prefix=prefix,
                                          redis_db=int(database))
            reg.get_dict(dictionary)
        except MissingArgumentError:
            raise
        except Exception:
            self.logger.error(traceback.format_exc())
            self.send_error(500)

    def delete(self, database, prefix, registry, dictionary):
        try:
            reg = Registry.find_or_create(registry,
                                          key_prefix=prefix,
                                          redis_db=int(database))
            if dictionary not in reg.dictionaries():
                return self.send_error(400)
            if not reg.del_dict(dictionary):
                return self.send_error(500)
        except MissingArgumentError:
            raise
        except Exception:
            self.logger.error(traceback.format_exc())
            self.send_error(500)


class LanguageHandler(LoggingMixin, RequestHandler):
    """
    Handler for the language dictionary of an entity
    """
    def entity(self, database, prefix, registry, dictionary):
        reg = Registry.find_or_create(registry,
                                      key_prefix=prefix,
                                      redis_db=int(database))
        if dictionary not in reg.dictionaries():
            return None
        entity_dictionary = reg.get_dict(dictionary)
        return entity_dictionary

    def get(self, database, prefix, registry, dictionary, language):
        try:
            entity_dictionary = self.entity(database, prefix, registry,
                                            dictionary)
            if entity_dictionary is None:
                return self.send_error(400)
            self.write(json_encode(
                {'count': entity_dictionary.cardinality(language)})
            )
        except MissingArgumentError:
            raise
        except Exception:
            self.logger.error(traceback.format_exc())
            self.send_error(500)

    def post(self, database, prefix, registry, dictionary, language):
        try:
            entity_dictionary = self.entity(database, prefix, registry,
                                            dictionary)
            if entity_dictionary is None:
                return self.send_error(400)
            entity_dictionary.add_language(language)
        except MissingArgumentError:
            raise
        except Exception:
            self.logger.error(traceback.format_exc())
            self.send_error(500)

    def put(self, database, prefix, registry, dictionary, language):
        try:
            entity_dictionary = self.entity(database, prefix, registry,
                                            dictionary)
            if entity_dictionary is None:
                return self.send_error(400)
            data = json_decode(self.request.body)
            if 'new_name' in data:
                entity_dictionary.change_language(language, data['new_name'])
        except MissingArgumentError:
            raise
        except Exception:
            self.logger.error(traceback.format_exc())
            self.send_error(500)

    def delete(self, database, prefix, registry, dictionary, language):
        try:
            entity_dictionary = self.entity(database, prefix, registry,
                                            dictionary)
            if entity_dictionary is None:
                return self.send_error(400)
            entity_dictionary.delete_language(language)
        except MissingArgumentError:
            raise
        except Exception:
            self.logger.error(traceback.format_exc())
            self.send_error(500)


class TermsHandler(LanguageHandler):
    """
    Handler for listing terms for a language of an entity
    """
    def get(self, database, prefix, registry, dictionary, language):
        try:
            entity_dictionary = self.entity(database, prefix, registry,
                                            dictionary)
            if entity_dictionary is None:
                return self.send_error(400)
            page = int(self.get_argument('page', 0))
            count = int(self.get_argument('count', 10))
            self.write(json_encode(
                {'terms': entity_dictionary.terms(language, page, count)})
            )
        except MissingArgumentError:
            raise
        except Exception:
            self.logger.error(traceback.format_exc())
            self.send_error(500)

    def post(self, database, prefix, registry, dictionary, language):
        try:
            entity_dictionary = self.entity(database, prefix, registry,
                                            dictionary)
            if entity_dictionary is None:
                return self.send_error(400)
            data = json_decode(self.request.body)
            if 'terms' in data:
                entity_dictionary.load_list(data['terms'], language)
        except MissingArgumentError:
            raise
        except Exception:
            self.logger.error(traceback.format_exc())
            self.send_error(500)

    def put(self, database, prefix, registry, dictionary, language):
        return self.post(database, prefix, registry, dictionary, language)

    def delete(self, database, prefix, registry, dictionary, language):
        try:
            entity_dictionary = self.entity(database, prefix, registry,
                                            dictionary)
            if entity_dictionary is None:
                return self.send_error(400)
            if self.request.body is not None:
                data = json_decode(self.request.body)
                if 'terms' in data:
                    for term in data['terms']:
                        if not entity_dictionary.delete_term(term, language):
                            self.send_error(500)
                else:
                    return self.send_error(500)
            else:
                # delete all terms
                pass
        except MissingArgumentError:
            raise
        except Exception:
            self.logger.error(traceback.format_exc())
            self.send_error(500)


class TermHandler(LanguageHandler):
    """
    Handler for managing a term
    """
    def get(self, database, prefix, registry, dictionary, language, term):
        try:
            self.write(term)
        except MissingArgumentError:
            raise
        except Exception:
            self.logger.error(traceback.format_exc())
            self.send_error(500)

    def post(self, database, prefix, registry, dictionary, language, term):
        try:
            entity_dictionary = self.entity(database, prefix, registry,
                                            dictionary)
            if entity_dictionary is None:
                return self.send_error(400)
            entity_dictionary.load_list([term], language)
        except MissingArgumentError:
            raise
        except Exception:
            self.logger.error(traceback.format_exc())
            self.send_error(500)

    def delete(self, database, prefix, registry, dictionary, language, term):
        try:
            entity_dictionary = self.entity(database, prefix, registry,
                                            dictionary)
            if entity_dictionary is None:
                return self.send_error(400)
            if not entity_dictionary.delete_term(term, language):
                self.send_error(500)
        except MissingArgumentError:
            raise
        except Exception:
            self.logger.error(traceback.format_exc())
            self.send_error(500)


class ExtractHandler(LoggingMixin, RequestHandler):
    """
    Handler for extract_entities endpoint
    Extracts from a text a list of terms that are part of a dictionary
    Input parameters in POST request:
        Mandatory parameters: text, entity_name
        Optional parameter: lang (default is 'en'), database (0), prefix (feet)
    """
    def post(self, database, prefix, registry, dictionary, language):
        try:
            data = json_decode(self.request.body)
            reg = Registry(registry, key_prefix=prefix, redis_db=int(database))
            entity_dictionary = reg.get_dict(dictionary)
            if entity_dictionary is None:
                return self.send_error(400)
            if 'text' not in data:
                return self.send_error(500)
            res = self.extract_entities(entity_dictionary,
                                        language,
                                        data['text'],
                                        data.get('grammar', None))
            self.write(json_encode({'result': res}))
        except MissingArgumentError:
            raise
        except Exception:
            self.logger.error(traceback.format_exc())
            self.send_error(500)

    def extract_entities(self, entity_dictionary, language, text, grammar):
        engine = Extractor(entity_dictionary, grammar)
        res = engine.extract(text, language)
        entities = []
        for element in res[0]:
            if element['entity_found'] == 1:
                entities = list(set(entities).union(
                    element['entity_candidates']))
        return entities
