#!/usr/bin/env python3
"""contains Cache class"""
import redis
from uuid import uuid4


class Cache:
    """defines a Cache class for caching with Redis"""
    def __init__():
        """constructor function"""
        self._redis = redis.Redis()
        self.redi.flushdb()

    def store(data: Union[str, bytes, int, float]) -> str:
        """generate a random key (e.g. using uuid).
           It stores the input data in Redis using the random key
           and return the key.
        """
        key = str(uuid4())
        self._redis.set(key, data)
        return key
