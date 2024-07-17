#!/usr/bin/env python3
'''List Documents.'''


def list_all(mongo_collection):
    '''List Collections Documents.'''
    return [doc for doc in mongo_collection.find()]
