#!/usr/bin/python3
"""cach module"""

import redis
import uuid
from typing import Union


class Cache:
    """ Initializes a Cache object with a Redis client instance. shift + 2 arrows"""

    def __init__(self):
        """ constructor """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in redis"""
        rnd_key = str(uuid.uuid4())
        self._redis.set(rnd_key, data)
        return rnd_key


if __name__ == "__main__":
    cache = Cache()

    data = b"hello"
    key = cache.store(data)
    print(key)

    local_redis = redis.Redis()
    print(local_redis.get(key))
