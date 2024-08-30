#!/usr/bin/env python3
"""contains Cache class"""
from functools import wraps
from typing import Callable, Union, Optional
from uuid import uuid4
import redis


def count_calls(method: Callable) -> Callable:
    """returns a Callable"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """handles the increment each time a method is called"""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """returns a Callable"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """handles saving input and output"""
        input_key = method.__qualname__ + ":inputs"
        output_key = method.__qualname__ + ":outputs"

        self._redis.rpush(input_key, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(output_key, result)

        return result

    return wrapper


def replay(func: Callable):
    """display the history of calls of a particular function"""
    cache = redis.Redis()

    func_name = func.__qualname__
    count = cache.get(func_name)
    n = 0 if not count else int(count.decode())
    print('{} was called {} time{}{}'.format(func_name, n,
                                             '' if n == 1 else 's',
                                             ':' if n else ''))

    if n:
        inputs = cache.lrange(func_name + ':inputs', 0, -1)
        outputs = cache.lrange(func_name + ':outputs', 0, -1)

        combined = zip(inputs, outputs)

        for each in combined:
            # Cache.store(*('foo',)) -> 13bf32a9-a249-4664-95fc-b1062db2038f
            print('{}(*{}) -> {}'.format(func_name,
                                         each[0].decode(),
                                         each[1].decode()))


class Cache:
    """defines a Cache class for caching with Redis"""
    def __init__(self):
        """constructor function"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """generate a random key (e.g. using uuid).
           It stores the input data in Redis using the random key
           and return the key.
        """
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """take a key (str) and an optional Callable argument named fn.
           fn will be used to convert the data back to the desired format.
        """
        value = self._redis.get(key)
        return fn(value) if value and fn else value

    def get_str(self, key: str) -> Optional[str]:
        """converts the result of the get method
           when it is bytes to a string
        """
        return self.get(key, lambda x: x.decode())

    def get_int(self, key: str) -> Optional[int]:
        """converts the result of the get method
           when it is an int to an int
        """
        return self.get(key, lambda x: int(x))
