#!/usr/bin/env python3
"""script that provides some stats about Nginx logs stored in MongoDB"""
from pymongo import MongoClient


db = MongoClient()
nginx = db.logs.nginx

print(nginx.count_documents(), 'logs')
print('Methods:')
method = ["GET", "POST", "PUT", "PATCH", "DELETE"]
for m in method:
    print(f'\tmethod {m}:', nginx.count_documents({'method': f'{m}'}))
print(nginx.count_documents({'path': '/status'}), 'status check')
