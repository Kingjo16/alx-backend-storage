#!/usr/bin/env python3
"""
Module to print statistics about Nginx request logs stored in MongoDB.
"""

from pymongo import MongoClient


def print_nginx_request_logs(nginx_collection):
    """
    Prints statistics about Nginx request logs.

    Args:
        nginx_collection (pymongo.collection.Collection): The
        MongoDB collection containing Nginx logs.
    """
    log_count = nginx_collection.count_documents({})
    print(f'{log_count} logs')
    
    print('Methods:')
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    for method in methods:
        req_count = nginx_collection.count_documents({'method': method})
        print(f'\tmethod {method}: {req_count}')
    
    status_check_count = nginx_collection.count_documents({'method': 'GET', 'path': '/status'})
    print(f'{status_check_count} status check')


def print_top_ips(nginx_collection):
    """
    Prints the top 10 IPs by request count in the Nginx logs.

    Args:
        nginx_collection (pymongo.collection.Collection):
        The MongoDB collection containing Nginx logs.
    """
    print('IPs:')
    request_logs = nginx_collection.aggregate([
        {'$group': {'_id': "$ip", 'totalRequests': {'$sum': 1}}},
        {'$sort': {'totalRequests': -1}},
        {'$limit': 10}
    ])
    for request_log in request_logs:
        ip = request_log['_id']
        ip_requests_count = request_log['totalRequests']
        print(f'\t{ip}: {ip_requests_count}')


def run():
    """
    Connects to the MongoDB server, retrieves 
    the Nginx logs collection, and prints statistics.
    """
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx
    print_nginx_request_logs(nginx_collection)
    print_top_ips(nginx_collection)


if __name__ == '__main__':
    run()

