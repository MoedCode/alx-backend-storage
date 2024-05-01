#!/usr/bin/python3
"""
function that list all document
"""
import pymongo


def list_all(mongo_collection):
    """
    list all collections
    """
    if not mongo_collection:
        return []
    return list(mongo_collection.find())
