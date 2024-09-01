#!/usr/bin/env python3
"""contains get_page function"""
import redis
import requests


def get_page(url: str) -> str:
    """uses the requests module to obtain the HTML content of a particular URL
       and returns it.
    """
    cache = redis.Redis()

    key_cache = f"cache:{url}"
    cache_result = cache.get(key_cache)

    key_count = f"count:{url}"
    cache.incr(key_count)

    if cache_result:
        return cache_result.decode()

    response = requests.get(url)
    cache.setex(key_cache, 10, response.text)

    return response.text


if __name__ == "__main__":
    get_page("http://slowwly.robertomurray.co.uk")
