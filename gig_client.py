"""
https://docs.python.org/3/library/argparse.html#the-add-argument-method
https://rich.readthedocs.io/en/stable/tables.html
"""

import argparse
from urllib.parse import urljoin
import os
import requests
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

    def _put(self, uri, data):
        response = self.session.put(urljoin(self.host, uri), json=data)
        assert response.status_code == 204

    def _delete(self, uri):
        response = self.session.delete(urljoin(self.host, uri))
        assert response.status_code == 204
    
    def list_users(self):
        return self._get("/gigwork/api/users")
    def list_postings(self):
        return self._get("/gigwork/api/postings")
    def list_gigs(self):
        return self._get("/gigwork/api/gigs")
    
    def get_user(self, pk):
        return self._get(f"/gigwork/api/users/{pk}/")
    def get_posting(self, pk):
        return self._get(f"/gigwork/api/postings/{pk}/")
    def get_gig(self, pk):
        return self._get(f"/gigwork/api/gigs/{pk}/")
    
    def create_user(self, data):
        return self._post("/gigwork/api/users/", data)
    def create_posting(self, data):
        return self._post("/gigwork/api/postings/", data)
    def create_gig(self, data):
        return self._post("/gigwork/api/gigs/", data)
    
    def update_user(self, pk, data):
        return self._put(f"/gigwork/api/users/{pk}/", data)
    def update_posting(self, pk, data):
        return self._put(f"/gigwork/api/postings/{pk}/", data)
    def update_gig(self, pk, data):
        return self._put(f"/gigwork/api/gigs/{pk}/", data)
    
    def delete_user(self, pk, data):
        return self._put(f"/gigwork/api/users/{pk}/", data)
    def delete_posting(self, pk, data):
        return self._put(f"/gigwork/api/postings/{pk}/", data)
    def delete_gig(self, pk, data):
        return self._put(f"/gigwork/api/gigs/{pk}/", data)

def print_users(client):

    table = Table(title="List of Users")
    table.add_column("ID", justify="center", style="cyan", no_wrap=True)
    table.add_column("First Name", justify="left", style="magenta")
    table.add_column("Last Name", justify="left", style="green")
    table.add_column("Email", justify="left", style="blue")
    table.add_column("Phone Number", justify="left", style="red")
    table.add_column("Address", justify="left", style="yellow")

    response = client.list_users()
    users = response.get("items")

    for user in users:
        table.add_row(
            str(user.get("id", None)),
            user.get("first_name", None),
            user.get("last_name", None),
            user.get("email", None),
            user.get("phone_number", None),
            user.get("address", None)
        )
    return table

if __name__ ==  "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("resource", help="")
    parser.add_argument("--list", action='store_true', help="")
    parser.add_argument("--create", action='store_true', help="")
    parser.add_argument("--retrieve", action='store_true', help="")
    parser.add_argument("--update", action='store_true', help="")
    parser.add_argument("--delete", action='store_true', help="")
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

            if args.resource == 'users':
                if args.list:
                    console = Console()
                    console.print(print_users(api))
