#!/usr/bin/env python3
"""script that provides some stats about Nginx logs stored in MongoDB"""
from pymongo import MongoClient


def get_stats():
    """a function that gets stats about Nginx logs in MongoDB"""
    db = MongoClient()
    nginx = db.logs.nginx

    print(nginx.count_documents({}), 'logs')
    print('Methods:')
    for method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        count = nginx.count_documents({'method': method})
        print(f"\tmethod {method}: {count}")
        print(nginx.count_documents({'method': 'GET',
                                     'path': '/status'}), 'status check')
    pipeline = [
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    top_ips = nginx.aggregate(pipeline)
    print('IPs:')
    for ip in top_ips:
        print(f"\t{ip['_id']}: {ip['count']}")


if __name__ == '__main__':
    get_stats()
