#!/usr/bin/env python3
"""contains Cache class"""
from typing import Union, Optional
from uuid import uuid4
import redis


class Cache:
    """defines a Cache class for caching with Redis"""
    def __init__(self):
        """constructor function"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """generate a random key (e.g. using uuid).
           It stores the input data in Redis using the random key
           and return the key.
        """
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[func] = None) -> Union[str, bytes, int, float]:
        """take a key (str) and an optional Callable argument named fn.
           fn will be used to convert the data back to the desired format.
        """
        value = self._redis.get(key)
        return fn(value) if fn else value

    def get_str(self, key: str) -> str:
        """converts the result of the get method
           when it is bytes to a string
        """
        return self._redis.get(key).decode()

    def get_int(self, key: str) -> int:
        """converts the result of the get method
           when it is an int to an int
        """
        return int(self._redis.get(key).decode())
