#!/usr/bin/python3
import redis
import uuid
from typing import Any, Callable, Union
from functools import wraps

"""
    Cache class. In the __init__ method, store an instance of the Redis client as
    a private variable named _redis (using redis.Redis())
    and flush the instance using flushdb.
"""


def count_calls(method: Callable) -> Callable:
    """Decorator that counts how many times a function is called"""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator that stores the history of inputs
    and outputs for a function"""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function"""
        self._redis.rpush(f"{key}:inputs", str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(f"{key}:outputs", str(result))
        return result
    return wrapper


class Cache:
    """
    Initializes a Cache object with a Redis client instance.
    shift + 2 arrows
    """

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
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
