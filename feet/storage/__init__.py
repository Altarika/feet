# -*- coding: utf8 -*-
# Storage Mixin
#
# Author:   Romary Dupuis <romary.dupuis@altarika.com>
#
# Copyright (C) 2016 Romary Dupuis
# Licensed under the GNU LGPL v2.1 - http://www.gnu.org/licenses/lgpl.html

import redis
from feet.config import settings
from feet.utils.decorators import memoized
from feet.utils.singleton import SingletonMetaClass
from feet.utils.logger import LoggingMixin


class StoreException(Exception):
    pass


class StoreNotImplemented(StoreException):
    pass


class StorageAbstract(object):
    def exists(self, key):
        raise StoreNotImplemented("exists not implemented")

    def keys(self, pattern):
        raise StoreNotImplemented("keys not implemented")

    def get(self, key):
        raise StoreNotImplemented("get not implemented")

    def delete(self, key):
        raise StoreNotImplemented("delete not implemented")

    def incr(self, key):
        raise StoreNotImplemented("incr not implemented")

    def decr(self, key):
        raise StoreNotImplemented("decr not implemented")

    def sadd(self, key, value):
        raise StoreNotImplemented("sadd not implemented")

    def smembers(self, key):
        raise StoreNotImplemented("smember not implemented")

    def srem(self, key, value):
        raise StoreNotImplemented("srem not implemented")

    def lrange(self, key, start, end):
        raise StoreNotImplemented("lrange not implemented")

    def lrem(self, key, count, value):
        raise StoreNotImplemented("lrem not implemented")

    def rpush(self, key, value):
        raise StoreNotImplemented("rpush not implemented")

    def transaction(self, func, *watchs, **params):
        raise StoreNotImplemented("transaction not implemented")


class Storage(LoggingMixin):
    __metaclass__ = SingletonMetaClass

    def __init__(self,
                 redis_host=settings.database.host,
                 redis_port=settings.database.port,
                 redis_db=0):
        self._redis_host = redis_host
        self._redis_port = redis_port
        self._redis_db = redis_db

    @memoized
    def redis_server(self):
        self.logger.info('Initialize storage service')
        return redis.StrictRedis(host=self._redis_host,
                                 port=self._redis_port,
                                 db=self._redis_db)

    def exists(self, key):
        return self.redis_server.exists(key)

    def keys(self, pattern):
        return self.redis_server.keys(pattern)

    def get(self, key):
        return self.redis_server.get(key)

    def delete(self, key):
        return self.redis_server.delete(key)

    def incr(self, key):
        return self.redis_server.incr(key)

    def decr(self, key):
        return self.redis_server.decr(key)

    def sadd(self, key, value):
        return self.redis_server.sadd(key, value)

    def smembers(self, key):
        return self.redis_server.smembers(key)

    def srem(self, key, value):
        return self.redis_server.srem(key, value)

    def lrange(self, key, start, end):
        return self.redis_server.lrange(key, start, end)

    def lrem(self, key, count, value):
        return self.redis_server.lrem(key, count, value)

    def rpush(self, key, value):
        return self.redis_server.rpush(key, value)

    def transaction(self, func, *watchs, **params):
        return self.redis_server.transaction(func, *watchs, **params)


class StorageMixin(object):
    """
    Mix in that provides storage capacity and singleton for storage
    """
    _redis_host = settings.database.host,
    _redis_port = settings.database.port,
    _redis_db = 0

    @memoized
    def storage(self):
        """
        Instantiates and returns a storage instance
        """
        return Storage(self._redis_host, self._redis_port, self._redis_db)
