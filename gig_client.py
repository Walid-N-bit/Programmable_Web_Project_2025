"""
CLI client to communicate with the gigwork API.
it supports GET, POST, PUT, DELETE requests through a set of actions:
GET: list, retrieve, filter
POST: create
PUT: update
DELETE: delete

sources:
https://lovelace.oulu.fi/ohjelmoitava-web/ohjelmoitava-web/exercise-4-implementing-hypermedia-clients/
https://docs.python.org/3/library/argparse.html#the-add-argument-method
https://rich.readthedocs.io/en/stable/tables.html
https://www.geeksforgeeks.org/python-unpack-list/
https://www.geeksforgeeks.org/python-ways-to-convert-string-to-json-object/
"""

import argparse
from urllib.parse import urljoin
import json
import requests
from rich.pretty import pprint
from rich.console import Console
from rich.table import Table

API_ROOT = "gigwork/api/root/"


class APIDataSource:
    """
    generic API class
    """

    def __init__(self, host, ca_cert=None, tkn=None):
        assert host.startswith("http"), "No protocol in host address"
        self.host = host
        self.session = requests.Session()
        if ca_cert:
            self.session.verify = ca_cert
        if tkn:
            self.session.headers.update({"Authorization": tkn})

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

    def get(self, uri):
        return self._get(uri)

    def post(self, uri, data):
        return self._post(uri, data)

    def put(self, uri, data):
        return self._put(uri, data)

    def delete(self, uri):
        return self._delete(uri)


def get_root_uri(host_uri):
    """
    return root URI of the API
    """
    return urljoin(host_uri, API_ROOT)


def get_users_uri(client, root):
    """
    return the URI for users
    """
    response = client.get(root)
    return response.get("@controls").get("users").get("href")


def get_postings_uri(client, root):
    """
    return the URI for postings
    """
    response = client.get(root)
    return response.get("@controls").get("postings").get("href")


def get_gigs_uri(client, root):
    """
    return the URI for gigs
    """
    response = client.get(root)
    return response.get("@controls").get("gigs").get("href")


def list_table(data, res):
    """
    create and return a Table() object containing response data
    of a collection resource.
    """
    table = Table(title=f"List of {res}", show_lines=True)
    items = data.get("items")
    for key in items[0].keys():
        table.add_column(key, justify="left", no_wrap=False)
    for item in items:
        row = [str(item.get(k, "")) for k in items[0].keys()]
        table.add_row(*row)
    return table


def retrieve_instance(data):
    """
    create and return a Table() object containing response data
    of a resource instance.
    """
    table = Table()
    item = data
    for key in item.keys():
        table.add_column(key, justify="left")
    row = [str(item.get(k, "")) for k in item.keys()]
    table.add_row(*row)
    return table


def print_list(data, res, is_json):
    """display list data either in table or json formats"""
    console = Console()
    if is_json:
        pprint(data)
    else:
        out = list_table(data, res)
        console.print(out)


def print_instance(data, is_json):
    """display an instance data either in table or json formats"""
    console = Console()
    if is_json:
        pprint(data)
    else:
        out = retrieve_instance(data)
        console.print(out)


def create_token_file(resp):
    """create .token file using response data"""
    with open(".token", "w", encoding="utf-8") as file:
        file.write(f"Token {resp.get('Token', '')}")


def main():
    """main client function"""
    parser = argparse.ArgumentParser()
    parser.add_argument("host", dest="host", help="API host address")
    parser.add_argument(
        "resource", help="Collection resource name: users, postings, gigs"
    )
    parser.add_argument(
        "action",
        help="Operation to be applied to the resource: "
        "list, retrieve, create, update, delete, filter."
        "data format for filter: '?field_1=value_1,...'.",
    )
    parser.add_argument("--pk", dest="pk", help="Primary Key to resource instance")
    parser.add_argument(
        "--data", dest="data", help="Data to be used in create or update actions"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Include to print the output in json format."
        "default is printing in table format.",
    )
    parser.add_argument("--ca", dest="ca", default=None, help="CA certificate file")
    try:
        args = parser.parse_args()
    except SystemExit:
        # This except is needed for the checking to work
        pass
    else:
        try:
            with open(".token", encoding="utf-8") as tokenfile:
                token = tokenfile.read().strip()
        except FileNotFoundError:
            token = None

        with APIDataSource(args.host, args.ca, token) as api:
            root_uri = get_root_uri(args.host)

            if args.resource == "users":
                if args.action == "list":
                    users_uri = get_users_uri(api, root_uri)
                    resp = api.get(users_uri)
                    print_list(resp, args.resource, args.json)

                elif args.action == "retrieve":
                    users_uri = urljoin(get_users_uri(api, root_uri), args.pk + "/")
                    resp = api.get(users_uri)
                    print_instance(resp, args.json)

                elif args.action == "create":
                    users_uri = get_users_uri(api, root_uri)
                    input_data = json.loads(args.data)
                    resp = api.post(users_uri, input_data)
                    create_token_file(resp)
                    pprint(resp)

                elif args.action == "update":
                    users_uri = urljoin(get_users_uri(api, root_uri), args.pk + "/")
                    input_data = json.loads(args.data)
                    resp = api.put(users_uri, input_data)

                elif args.action == "delete":
                    users_uri = urljoin(get_users_uri(api, root_uri), args.pk + "/")
                    resp = api.delete(users_uri)

                elif args.action == "filter":
                    users_uri = urljoin(get_users_uri(api, root_uri), args.data)
                    resp = api.get(users_uri)
                    print_list(resp, args.resource, args.json)

            elif args.resource == "postings":
                if args.action == "list":
                    postings_uri = get_postings_uri(api, root_uri)
                    resp = api.get(postings_uri)
                    print_list(resp, args.resource, args.json)

                elif args.action == "retrieve":
                    postings_uri = urljoin(
                        get_postings_uri(api, root_uri), args.pk + "/"
                    )
                    resp = api.get(postings_uri)
                    print_instance(resp, args.json)

                elif args.action == "create":
                    postings_uri = get_postings_uri(api, root_uri)
                    input_data = json.loads(args.data)
                    resp = api.post(postings_uri, input_data)
                    pprint(resp)

                elif args.action == "update":
                    postings_uri = urljoin(
                        get_postings_uri(api, root_uri), args.pk + "/"
                    )
                    input_data = json.loads(args.data)
                    resp = api.put(postings_uri, input_data)

                elif args.action == "delete":
                    postings_uri = urljoin(
                        get_postings_uri(api, root_uri), args.pk + "/"
                    )
                    resp = api.delete(postings_uri)

                elif args.action == "filter":
                    postings_uri = urljoin(get_postings_uri(api, root_uri), args.data)
                    resp = api.get(postings_uri)
                    print_list(resp, args.resource, args.json)

            elif args.resource == "gigs":
                if args.action == "list":
                    gigs_uri = get_gigs_uri(api, root_uri)
                    resp = api.get(gigs_uri)
                    print_list(resp, args.resource, args.json)

                elif args.action == "retrieve":
                    gigs_uri = urljoin(get_gigs_uri(api, root_uri), args.pk + "/")
                    resp = api.get(gigs_uri)
                    print_instance(resp, args.json)

                elif args.action == "create":
                    gigs_uri = get_gigs_uri(api, root_uri)
                    input_data = json.loads(args.data)
                    resp = api.post(gigs_uri, input_data)
                    pprint(resp)

                elif args.action == "update":
                    gigs_uri = urljoin(get_gigs_uri(api, root_uri), args.pk + "/")
                    input_data = json.loads(args.data)
                    resp = api.put(gigs_uri, input_data)

                elif args.action == "delete":
                    gigs_uri = urljoin(get_gigs_uri(api, root_uri), args.pk + "/")
                    resp = api.delete(gigs_uri)

                elif args.action == "filter":
                    gigs_uri = urljoin(get_gigs_uri(api, root_uri), args.data)
                    resp = api.get(gigs_uri)
                    print_instance(resp, args.json)


if __name__ == "__main__":
    main()
