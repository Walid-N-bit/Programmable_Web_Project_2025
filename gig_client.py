"""
https://docs.python.org/3/library/argparse.html#the-add-argument-method
https://rich.readthedocs.io/en/stable/tables.html
https://www.geeksforgeeks.org/python-unpack-list/
https://www.geeksforgeeks.org/python-ways-to-convert-string-to-json-object/
"""

import argparse
from urllib.parse import urljoin
import os
import requests
import json
from rich.pretty import pprint
from rich.console import Console
from rich.table import Table

API_ROOT = "gigwork/api/root/"

class APIDataSource:
    """
    generic API class
    """
    def __init__(self, host, ca_cert=None, api_key=None):
        assert host.startswith("http"), "No protocol in host address"
        self.host = host
        self.session = requests.Session()
        if ca_cert:
            self.session.verify = ca_cert
        if api_key:
            self.session.headers.update({"Authorization": api_key})

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.session.close()

    def _get(self, uri):
        response = self.session.get(urljoin(self.host, uri))
        assert response.status_code == 200
        return response.json()
    
    def _post(self, uri, data):
        response = self.session.post(urljoin(self.host, uri), json=data)
        assert response.status_code == 201
        return response.json()

    def _put(self, uri, data):
        response = self.session.put(urljoin(self.host, uri), json=data)
        assert response.status_code == 200

    def _delete(self, uri):
        response = self.session.delete(urljoin(self.host, uri))
        assert response.status_code == 204

def get_root_uri(host_uri):
    return urljoin(host_uri, API_ROOT)  

def get_users_uri(client, root):
    response = client._get(root)
    return response.get('@controls').get('users').get('href')
def get_postings_uri(client, root):
    response = client._get(root)
    return response.get('@controls').get('postings').get('href')
def get_gigs_uri(client, root):
    response = client._get(root)
    return response.get('@controls').get('gigs').get('href')

def list_table(data, res):
    table = Table(title=f"List of {res}")
    items = data.get("items")
    for key in items[0].keys():
        table.add_column(key, justify='left')    
    for item in items:
        row = [str(item.get(k,"")) for k in items[0].keys()]
        table.add_row(*row)
    return table

def retrieve_instance(data):
    table = Table()
    item = data
    for key in item.keys():
        table.add_column(key, justify='left')  
    row = [str(item.get(k,"")) for k in item.keys()]
    table.add_row(*row)
    return table

def print_list(data, res, is_json):
    console = Console()
    if is_json:
        pprint(data)
    else:
        out = list_table(data, res)
        console.print(out)
def print_instance(data, is_json):
    console = Console()
    if is_json:
        pprint(data)
    else:
        out = retrieve_instance(data)
        console.print(out)

if __name__ ==  "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("resource", help="")
    parser.add_argument("--pk", dest='pk', help="")
    parser.add_argument("--data", dest='data', help="")
    parser.add_argument("--json", action='store_true', help="")
    parser.add_argument("command", help="")
    parser.add_argument("--host", dest="host", help="API host address")
    parser.add_argument("--ca", dest="ca", default=None, help="CA certificate file")
    try:
        args = parser.parse_args()
    except SystemExit:
        # This except is needed for the checking to work
        pass
    else:
        try:
            with open(".apikey") as keyfile:
                key = keyfile.read().strip()
        except FileNotFoundError:
            key = None
        
        with APIDataSource(args.host, args.ca, key) as api:
            root_uri = get_root_uri(args.host)
            
            if args.resource == 'users':
                if args.command == 'list':
                    uri = get_users_uri(api, root_uri)
                    response = api._get(uri)
                    print_list(response, args.resource, args.json)

                elif args.command == 'retrieve':
                    uri = urljoin(get_users_uri(api, root_uri), args.pk+'/')
                    response = api._get(uri)
                    print_instance(response, args.json)

                elif args.command == 'create':
                    uri = get_users_uri(api, root_uri)
                    data = json.loads(args.data)
                    response = api._post(uri, data)
                    pprint(response)

                elif args.command == 'update':
                    uri = urljoin(get_users_uri(api, root_uri), args.pk+'/')
                    data = json.loads(args.data)
                    response = api._put(uri, data)

                elif args.command == 'delete':
                    uri = urljoin(get_users_uri(api, root_uri), args.pk+'/')
                    response = api._delete(uri)

            elif args.resource == 'postings':
                if args.command == 'list':
                    uri = get_postings_uri(api, root_uri)
                    response = api._get(uri)
                    print_list(response, args.resource, args.json)

                elif args.command == 'retrieve':
                    uri = urljoin(get_postings_uri(api, root_uri), args.pk+'/')
                    response = api._get(uri)
                    print_instance(response, args.json)

                elif args.command == 'create':
                    uri = get_postings_uri(api, root_uri)
                    data = json.loads(args.data)
                    response = api._post(uri, data)
                    pprint(response)

                elif args.command == 'update':
                    uri = urljoin(get_postings_uri(api, root_uri), args.pk+'/')
                    data = json.loads(args.data)
                    response = api._put(uri, data)
                    
                elif args.command == 'delete':
                    uri = urljoin(get_postings_uri(api, root_uri), args.pk+'/')
                    response = api._delete(uri)

            elif args.resource == 'gigs':
                if args.command == 'list':
                    uri = get_gigs_uri(api, root_uri)
                    response = api._get(uri)
                    print_list(response, args.resource, args.json)

                elif args.command == 'retrieve':
                    uri = urljoin(get_gigs_uri(api, root_uri), args.pk+'/')
                    response = api._get(uri)
                    print_instance(response, args.json)

                elif args.command == 'create':
                    uri = get_gigs_uri(api, root_uri)
                    data = json.loads(args.data)
                    response = api._post(uri, data)
                    pprint(response)

                elif args.command == 'update':
                    uri = urljoin(get_gigs_uri(api, root_uri), args.pk+'/')
                    data = json.loads(args.data)
                    response = api._put(uri, data)
                    
                elif args.command == 'delete':
                    uri = urljoin(get_gigs_uri(api, root_uri), args.pk+'/')
                    response = api._delete(uri)
