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
https://www.geeksforgeeks.org/python-program-to-remove-last-character-from-the-string/
"""
import os
import argparse
import json
from urllib.parse import urljoin
from yaml import safe_load
import requests
from rich.console import Console
from rich.pretty import pprint
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

    def get(self, uri):
        """
        HTTP GET request
        """
        response = self.session.get(urljoin(self.host, uri))
        assert response.status_code == 200
        return response.json()

    def post(self, uri, data):
        """
        HTTP POST request
        """
        response = self.session.post(urljoin(self.host, uri), json=data)
        assert response.status_code == 201
        return response.json()

    def put(self, uri, data):
        """
        HTTP PUT request
        """
        response = self.session.put(urljoin(self.host, uri), json=data)
        assert response.status_code == 200
        return response.json()

    def delete(self, uri):
        """
        HTTP DELETE request
        """
        response = self.session.delete(urljoin(self.host, uri))
        assert response.status_code == 204

    def get_schema(self, uri):
        """
        HTTP GET request for yaml schema
        """
        response = self.session.get(urljoin(self.host, uri))
        assert response.status_code == 200
        return safe_load(response.text)


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


def get_schema_uri(client, root):
    """
    return the URI for gigs
    """
    response = client.get(root)
    return response.get("@controls").get("schema").get("href")


def list_table(data, res):
    """
    create and return a Table() object containing response data
    of a collection resource.
    """
    table = Table(title=f"List of {res}", show_lines=True)
    items = data.get("items")
    colors = ['white', 'red', 'yellow',
              'green', 'blue', 'cyan',
              'magenta', 'purple', 'green',
              'blue', 'cyan', 'yellow']
    for key, color in zip(items[0].keys(), colors):
        table.add_column(key, justify="left", no_wrap=False, style=color)
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
    """
    display list data either in table or json formats
    """
    console = Console()
    if is_json:
        pprint(data)
    else:
        out = list_table(data, res)
        console.print(out)


def print_instance(data, is_json):
    """
    display an instance data either in table or json formats
    """
    console = Console()
    if is_json:
        pprint(data)
    else:
        out = retrieve_instance(data)
        console.print(out)


def create_token_file(resp):
    """
    create .token file using response data
    """
    with open(".token", "w", encoding="utf-8") as file:
        file.write(f"Token {resp.get('Token', '')}")

def get_resource_keys(client, uri, resource):
    """
    return list of keys for the given resource model
    """
    schema = client.get_schema(uri)
    schemas = schema.get('components', {}).get('schemas', {})
    props = {}
    if resource == "users":
        props = schemas.get('User').get('properties', {})
    elif resource == "postings":
        props = schemas.get('Posting').get('properties', {})
    elif resource == "gigs":
        props = schemas.get('Gig').get('properties', {})

    keys = list(props.keys())
    auto_fields = [
        'id',
        'owner',
        'created_at',
        'expires_at',
        'start_date',
        'end_date',
        '@controls']
    for field in auto_fields:
        if field in keys:
            keys.remove(field)
    return keys

def data_input(keys):
    """
    prompt user to input value for each key
    """
    pprint("Please input necessary data:")
    data = {}
    for key in keys:
        value = input(f"{key}: ")
        if value:
            data[key] = value

    price = data.get('price')
    if price:
        data['price'] = float(price)
    posting = data.get('posting')
    if posting:
        data['posting'] = int(posting)
    return data

def filter_data_str(data, keys):
    """
    return a query string
    """
    fltr = "?"
    for key in keys:
        value = data.get(key)
        if value:
            fltr += f"{key}={value},"
    return fltr[:-1]


def list_func(client, uri, resource, is_json):
    """
    handler function for list action
    """
    response = client.get(uri)
    print_list(response, resource, is_json)


def retrieve_func(client, uri, pk, is_json):
    """
    handler function for retrieve action
    """
    full_uri = urljoin(uri, pk + "/")
    response = client.get(full_uri)
    print_instance(response, is_json)


def create_func(client, uri, keys, res):
    """
    handler function for create action
    """
    input_data = data_input(keys)
    response = client.post(uri, input_data)
    if res == 'users':
        create_token_file(response)
    pprint(response)


def update_func(client, uri, pk, keys):
    """
    handler function for update action
    """
    full_uri = urljoin(uri, pk + "/")
    data = data_input(keys)
    client.put(full_uri, data)


def delete_func(client, uri, pk):
    """
    handler function for delete action
    """
    full_uri = urljoin(uri, pk + "/")
    client.delete(full_uri)


def filter_func(client, uri, keys, resource, is_json):
    """
    handler function for filter action
    """
    data = data_input(keys)
    filter_str = filter_data_str(data, keys)
    full_uri = urljoin(uri, filter_str)
    response = client.get(full_uri)
    print_list(response, resource, is_json)


def main():
    """main client function"""
    parser = argparse.ArgumentParser()
    parser.add_argument("host", help="API host address")
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
            schema_uri = get_schema_uri(api, root_uri)

            if args.resource == "users":
                keys = get_resource_keys(api, schema_uri, args.resource)
                users_uri = get_users_uri(api, root_uri)
                if args.action == "list":
                    list_func(api, users_uri, args.resource, args.json)

                elif args.action == "retrieve":
                    retrieve_func(api, users_uri, args.pk, args.json)

                elif args.action == "create":
                    create_func(api, users_uri, keys, args.resource)

                elif args.action == "update":
                    update_func(api, users_uri, args.pk, keys)

                elif args.action == "delete":
                    delete_func(api, users_uri, args.pk)
                    os.remove('.token')

                elif args.action == "filter":
                    filter_func(api, users_uri, keys, args.resource, args.json)


            elif args.resource == "postings":
                keys = get_resource_keys(api, schema_uri, args.resource)
                postings_uri = get_postings_uri(api, root_uri)
                if args.action == "list":
                    list_func(api, postings_uri, args.resource, args.json)

                elif args.action == "retrieve":
                    retrieve_func(api, postings_uri, args.pk, args.json)

                elif args.action == "create":
                    create_func(api, postings_uri, keys, args.resource)

                elif args.action == "update":
                    update_func(api, postings_uri, args.pk, keys)

                elif args.action == "delete":
                    delete_func(api, postings_uri, args.pk)

                elif args.action == "filter":
                    filter_func(api, postings_uri, keys, args.resource, args.json)


            elif args.resource == "gigs":
                keys = get_resource_keys(api, schema_uri, args.resource)
                gigs_uri = get_gigs_uri(api, root_uri)
                if args.action == "list":
                    list_func(api, gigs_uri, args.resource, args.json)

                elif args.action == "retrieve":
                    retrieve_func(api, gigs_uri, args.pk, args.json)

                elif args.action == "create":
                    create_func(api, gigs_uri, keys, args.resource)

                elif args.action == "update":
                    update_func(api, gigs_uri, args.pk, keys)

                elif args.action == "delete":
                    delete_func(api, gigs_uri, args.pk)

                elif args.action == "filter":
                    filter_func(api, gigs_uri, keys, args.resource, args.json)


if __name__ == "__main__":
    main()
