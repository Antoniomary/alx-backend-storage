#!/usr/bin/env python3
"""script that provides some stats about Nginx logs stored in MongoDB"""
from pymongo import MongoClient


def get_stats():
    db = MongoClient()
    nginx = db.logs.nginx

    print(nginx.count_documents(), 'logs')
    print('Methods:')
    for m in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        print(f"\tmethod {m}: {nginx.count_documents({'method': '{m}'})}")
    print(nginx.count_documents({'method': 'GET',
                                 'path': '/status'}), 'status check')


if __name__ == '__main__':
    get_stats()
