# -*- coding: utf8 -*-
# registry.py
# Manages a list of entities
#
# Author:   Romary Dupuis <romary.dupuis@altarika.com>
#
# Copyright (C) 2016 Romary Dupuis
# Licensed under the GNU LGPL v2.1 - http://www.gnu.org/licenses/lgpl.html

from feet.utils.logger import LoggingMixin
from feet.utils.decorators import memoized
from feet.entities.dictionary import Dictionary
from feet.config import settings
from feet.storage import Storage, StorageMixin


class Registry(StorageMixin, LoggingMixin):
    @staticmethod
    def registry_list_key(key_prefix):
        return '{}:registries'.format(key_prefix)

    @staticmethod
    def registry_key(key_prefix, name):
        return '{}:registry:{}'.format(key_prefix, name)

    @classmethod
    def list(klass,
             key_prefix=settings.database.prefix,
             redis_host=settings.database.host,
             redis_port=settings.database.port,
             redis_db=0):
        """
        Gets the list of registries under a prefix.
        """
        if key_prefix is None:
            return False
        storage = Storage(redis_host, redis_port, redis_db)
        return list(storage.smembers(klass.registry_list_key(key_prefix)))

    @classmethod
    def flush(klass,
              key_prefix=settings.database.prefix,
              redis_host=settings.database.host,
              redis_port=settings.database.port,
              redis_db=0):
        """
        Deletes all registries, dictionaries etc. under a prefix
        """
        if key_prefix is None:
            return False
        storage = Storage(redis_host, redis_port, redis_db)
        keys = storage.keys('{}:*'.format(key_prefix))
        for key in keys:
            storage.delete(key)
        return True

    @classmethod
    def find_or_create(klass,
                       name,
                       dict_class=Dictionary,
                       key_prefix=settings.database.prefix,
                       redis_host=settings.database.host,
                       redis_port=settings.database.port,
                       redis_db=0):
        """
        Finds a registry if it already exists otherwise creates it.
        """
        if key_prefix is None:
            return None
        storage = Storage(redis_host, redis_port, redis_db)
        storage.sadd(klass.registry_list_key(key_prefix), name)
        return Registry(name, dict_class, key_prefix,
                        redis_host, redis_port, redis_db)

    def __init__(self,
                 name,
                 dict_class=Dictionary,
                 key_prefix=settings.database.prefix,
                 redis_host=settings.database.host,
                 redis_port=settings.database.port,
                 redis_db=0):
        self._name = name
        self._dict_class = dict_class
        self._key_prefix = key_prefix
        self._redis_host = redis_host
        self._redis_port = redis_port
        self._redis_db = redis_db

    @memoized
    def key(self):
        return '{}'.format(self.registry_key(self._key_prefix,
                                             self._name))

    @memoized
    def dict_key(self):
        return '{}:dictionaries'.format(self.key)

    def dictionaries(self):
        """
        Gest list of dictionaries defined under a specific registry.
        """
        registry = self.storage.smembers(self.dict_key)
        return list(registry)

    def get_dict(self, name):
        """
        Adds or gets a dictionary under a specific registry.
        """
        # TODO: make a transaction here
        self.storage.sadd(self.dict_key, name)
        return self._dict_class(name, self.key, self._redis_host,
                                self._redis_port, self._redis_db)

    def del_dict(self, name):
        """
        Deletes a dictionary under a specific registry.
        """
        # TODO: make a transaction here
        if name not in self.dictionaries():
            return False
        dictionary = self._dict_class(name, self.key, self._redis_host,
                                      self._redis_port, self._redis_db)
        dictionary.delete()
        if self.storage.srem(self.dict_key, name) == 1:
            return True
        return False

    def delete(self):
        """
        Deletes the registry.
        """
        self.logger.info("Deleting registry %s ..." % self._name)
        if self.storage.srem(self.registry_list_key(self._key_prefix),
                             self._name) == 1:
            self.reset()
            self.logger.info("DONE")
            return True
        return False

    def reset(self):
        """
        Resets the registry. Automatically deletes related dictionaries.
        """
        if self.storage.delete(self.dict_key) == 1:
            self.logger.info("Deleting registry {} entities..."
                             .format(self._name))
            keys = self.storage.keys('{}:*'.format(self.key))
            for key in keys:
                self.storage.delete(key)
            self.logger.info("DONE")
            return True
        return False
