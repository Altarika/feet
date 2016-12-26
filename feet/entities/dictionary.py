# -*- coding: utf8 -*-
# dictionary.py
# Load and index terms into a Redis database
#
# Author:   Romary Dupuis <romary.dupuis@altarika.com>
#
# Copyright (C) 2016 Romary Dupuis
# Licensed under the GNU LGPL v2.1 - http://www.gnu.org/licenses/lgpl.html

import csv
from feet.config import settings
from feet.utils.logger import LoggingMixin
from feet.utils.decorators import memoized
from feet.entities.nlp import Parser
from feet.storage import StorageMixin


class Dictionary(StorageMixin, LoggingMixin):
    @staticmethod
    def dict_key(key_prefix, name):
        return '{}:entity:{}'.format(key_prefix, name)

    def __init__(self,
                 name,
                 key_prefix=settings.database.prefix,
                 redis_host=settings.database.host,
                 redis_port=settings.database.port,
                 redis_db=0):
        self._name = name
        self._key_prefix = key_prefix
        self._redis_host = redis_host
        self._redis_port = redis_port
        self._redis_db = redis_db

    @memoized
    def parser(self):
        return Parser()

    @memoized
    def key(self):
        return '{}:entity:{}'.format(self._key_prefix, self._name)

    def terms_list_key(self, lang):
        return '{}:lang:{}:terms'.format(
            self.key,
            self._name,
            lang)

    def term_key(self, lang, term):
        return '{}:lang:{}:term:{}'.format(
            self.key,
            lang,
            term.lower())

    def token_key(self, lang, token):
        return '{}:lang:{}:dictionary:{}'.format(
            self.key,
            lang,
            token.lower())

    def cardinality_key(self, lang):
        return '{}:lang:{}:cardinality'.format(
            self.key,
            lang)

    def languages_key(self):
        return '{}:languages'.format(
            self.key)

    def languages(self):
        try:
            return list(self.storage.smembers(self.languages_key()))
        except:
            return []

    def add_language(self, lang):
        if lang not in self.languages():
            if self.storage.sadd(self.languages_key(), lang) == 1:
                return True
        return False

    def change_language(self, lang, new_lang):
        self.add_language(new_lang)

    def cardinality(self, lang):
        try:
            return int(self.storage.get(self.cardinality_key(lang)))
        except:
            return 0

    def load_file(self, file_name, lang):
        self.logger.info("Loading entity file ... %s" % file_name)
        count = 0
        for term in self.parse_file(file_name):
            if self.add_term(term, lang):
                count += 1
        return count

    def parse_file(self, entities_file):
        handle = open(entities_file, "r")
        for term in handle.readlines():
            yield term

    def load_list(self, entities_list, lang):
        count = 0
        for term in entities_list:
            if self.add_term(term, lang):
                count += 1
        return count

    def add_term(self, term, lang):
        if isinstance(term, unicode):
            term = term.encode('utf8')
        self.logger.debug('Add term {}'.format(term))
        term = term.strip()
        self.add_language(lang)

        def add_term_transaction(pipe):
            if pipe.exists(self.term_key(lang, term)) == 0:
                pipe.rpush(self.terms_list_key(lang), term)
                tokens = self.parser.word_tokenize(term, lang)
                pipe.incr(self.cardinality_key(lang))
                for token in tokens:
                    pipe.sadd(self.term_key(lang, term), token)
                    pipe.sadd(self.token_key(lang, token),
                              term.lower())
                return True
            else:
                return False

        return self.storage.transaction(add_term_transaction,
                                        self.term_key(lang, term),
                                        value_from_callable=True)

    def delete_term(self, term, lang):
        if isinstance(term, unicode):
            term = term.encode('utf8')
        self.logger.debug('Delete term {}'.format(term))
        term = term.strip()
        if lang not in self.languages():
            return False
        if self.storage.exists(self.term_key(lang, term)) == 0:
            return False

        def delete_term_transaction(pipe):
            if pipe.delete(self.term_key(lang, term)) != 1:
                return False
            tokens = self.parser.word_tokenize(term, lang)
            for token in tokens:
                if pipe.srem(self.token_key(lang, token),
                             term.lower()) != 1:
                    return False
            pipe.lrem(self.terms_list_key(lang), 0, term)
            pipe.decr(self.cardinality_key(lang))
            return True

        return self.storage.transaction(delete_term_transaction,
                                        self.term_key(lang, term),
                                        value_from_callable=True)

    def exact_match(self, candidate, lang):
        return len(self.storage.smembers(
            self.term_key(lang, candidate))) > 0

    def candidates(self, token, lang):
        return self.storage.smembers(self.token_key(lang, token))

    def tokens(self, candidate, lang):
        return list(self.storage.smembers(
            self.term_key(lang, candidate)))

    def delete(self):
        """
        Deletes the dictionary.
        """
        self.logger.info("Deleting %s on redis..." % self._name)
        keys = self.storage.keys('{}:*'.format(self.key))
        for key in keys:
            self.storage.delete(key)
        self.logger.info("DONE")
        return True

    def delete_language(self, lang):
        self.logger.info("Deleting dictionary {} {} on redis...".format(
            self._name,
            lang))

        def delete_language_transaction(pipe):
            keys = pipe.keys('{}:lang:{}:*'.format(self.key, lang))
            for key in keys:
                pipe.delete(key)
            if pipe.srem(self.languages_key(), lang) == 1:
                self.logger.info("DONE")
                return True
            return False

        return self.storage.transaction(delete_language_transaction,
                                        self.languages_key(),
                                        value_from_callable=True)

    def terms(self, lang, page=0, count=10):
        return self.storage.lrange(self.terms_list_key(lang), page * count,
                                   (page + 1) * count - 1)


class CSVDictionary(Dictionary):
    def parse_file(self, file_name):
        """
        Easy parsing CSV file
        """
        first_line = True
        with open(file_name, 'rb') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                if first_line:
                    first_line = False
                    continue
                else:
                    yield row[0]
