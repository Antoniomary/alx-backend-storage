#!/usr/bin/env python3
"""contains the function list_all"""


def list_all(mongo_collection):
    """lists all documents in a collection"""
    return [each for each in mongo_collection.find()]
