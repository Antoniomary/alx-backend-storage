#!/usr/bin/env python3
"""contains get_page function"""
import redis
import requests


def get_page(url: str) -> str:
    """uses the requests module to obtain the HTML content of a particular URL
       and returns it.
    """
    response = requests.get(url)
    if response.ok:
        key = f"count:{url}"
        cache = redis.Redis()
        cache.setex(key, 10, response.text)
    return response.text
