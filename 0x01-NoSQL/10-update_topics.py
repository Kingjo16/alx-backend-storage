#!/usr/bin/env python3
'''Task Update.'''


def update_topics(mongo_collection, name, topics):
    '''Update topics of a collection's document based on the name.'''
    mongo_collection.update_many(
        {'name': name},
        {'$set': {'topics': topics}}
    )
