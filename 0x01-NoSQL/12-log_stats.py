#!/usr/bin/env python3
"""script that provides some stats about Nginx logs stored in MongoDB:"""


from pymongo import MongoClient


def log_stats(logs_collection):
    """
    Provides some stats about Nginx logs stored in MongoDB.

    Args:
        logs_collection: A pymongo collection object.

    """
    total = logs_collection.count_documents({})
    get = logs_collection.count_documents({"method": "GET"})
    post = logs_collection.count_documents({"method": "POST"})
    put = logs_collection.count_documents({"method": "PUT"})
    patch = logs_collection.count_documents({"method": "PATCH"})
    delete = logs_collection.count_documents({"method": "DELETE"})
    head = logs_collection.count_documents({"method": "HEAD"})
    connect = logs_collection.count_documents({"method": "CONNECT"})
    options = logs_collection.count_documents({"method": "OPTIONS"})
    top10 = logs_collection.aggregate([
        {"$group": {"_id": "$path", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])
    top10 = [{"path": doc["_id"], "count": doc["count"]} for doc in top10]
    return (total, get, post, put, patch, delete, head, connect, options, top10)


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    mongo_collection = client.logs.nginx
    print(f"{log_stats(mongo_collection)} logs")
