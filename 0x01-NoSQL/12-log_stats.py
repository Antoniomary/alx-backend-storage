#!/usr/bin/env python3
"""script that provides some stats about Nginx logs stored in MongoDB"""
from pymongo import MongoClient


def get_stats():
    db = MongoClient('mongodb://127.0.0.1:27017')
    nginx = db.logs.nginx

    print(nginx.count_documents({}), 'logs')
    print('Methods:')
    for method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        count = nginx.count_documents({'method': method})
        print(f"\tmethod {method}: {count}")
    print(nginx.count_documents({'method': 'GET',
                                 'path': '/status'}), 'status check')


if __name__ == '__main__':
    get_stats()
