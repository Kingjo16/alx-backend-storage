#!/usr/bin/env python3
'''Task Insert.'''


def insert_school(mongo_collection, **kwargs):
    '''Insert a doc in the collection.'''
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
