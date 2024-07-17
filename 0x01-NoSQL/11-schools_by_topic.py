#!/usr/bin/env python3
"""
Module to find schools by topic in a MongoDB collection.
"""

def schools_by_topic(mongo_collection, topic):
    """
    Returns a list of schools having a specific topic.

    Args:
        mongo_collection (pymongo.collection.Collection): The MongoDB collection containing school documents.
        topic (str): The topic to filter schools by.

    Returns:
        list: A list of schools that have the specified topic.
    """
    topic_filter = {
        'topics': topic
    }
    return list(mongo_collection.find(topic_filter))
