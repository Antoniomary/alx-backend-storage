#!/usr/bin/env python3
"""contains Cache class"""
from typing import Union
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
