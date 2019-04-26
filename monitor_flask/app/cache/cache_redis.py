import redis

from common_utils import MetaSingleton
from app.config import RedisConfig

class CacheRedis(metaclass=MetaSingleton):
    def __init__(self):
        self.__init_connection__()

    def __init_connection__(self):
        self._pool = redis.ConnectionPool(host=RedisConfig().host,
                                          port=RedisConfig().port,
                                          db=RedisConfig().db,
                                          password=RedisConfig().password
                                          )
        self._client = redis.StrictRedis(connection_pool=self._pool)


    def get(self, item):
        try:
            return self._client.get(item)
        except ConnectionError as e:
            pass

    def set(self,key,value):
        try:
            self._client.set(key,value)
        except ConnectionError as e:
            pass

    def delete(self,item):
        try:
            self._client.delete([item, ])
        except ConnectionError as e:
            pass

    def get_keys(self):
        try:
            return self._client.keys()
        except ConnectionError as e:
            pass

    def flushall(self):
        try:
            return self._client.flushall()
        except ConnectionError as e:
            pass
