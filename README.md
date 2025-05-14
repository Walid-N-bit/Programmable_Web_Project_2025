# PWP SPRING 2025
# PROJECT NAME
# Group information
* Student 1. Walid Nouicer,	Walid.Nouicer@student.oulu.fi
* Student 2. Abiola Ajibowu,	Abiola.Ajibowu@student.oulu.fi
* Student 3. Atte Viertola,	Atte.Viertola@student.oulu.fi


__Remember to include all required documentation and HOWTOs, including how to create and populate the database, how to run and test the API, the url to the entrypoint, instructions on how to setup and run the client, instructions on how to setup and run the axiliary service and instructions on how to deploy the api in a production environment__

## Database implementation

For the database model implementations, we decided to use Django.\
For database itself, SQLite3 was used with version 3.40.1, Django is version 5.1.6\
For testing just installing Django is enough:
```
python -m venv .testenv
source .testenv/bin/activate
pip install Django
```
A script populating the database is included in .../populatedb.py:
```
python manage.py makemigrations
python manage.py migrate
python manage.py shell < populatedb.py
```
This creates a file called db.sqlite3 that contains the db.\
Due to time constraints of other courses, there was no time to implement the DB in a proper framework, but this is definitely something that could still be done.

### Running the API

To start running the API:
```
python manage.py runserver
```
This will start the API at http://localhost:8000/

### Running tests:

Tests can be done using the provided script `testing_and_cov.ps1`.\
To run a specific test use:
```
coverage run --source='.' manage.py test tests.<test-name>
coverage report -m
```

### Using the client:

Basic command structure:
```
python gig_client.py <host-address> <resource> <action> 
```
This will perform the required operation (action) on the specified resource.

Arguments:
* `<host-address>` is the host address of the API.
* `<resource>` is either of the collection resources avalable: `users`, `postings`, `gigs`.
* `<action>` is either of the following actions: `list`, `retrieve`, `create`, `update`, `delete`, `filter`.
* `--pk` is needed to specify the primary key value of an isntance resource for `retrieve`, `update`, `delete` actions.
* `--json` can be included to print the output in JSON format.
* `--ca` is to include CA certificate file.

Example:
```
python gig_client.py http://localhost:8000/ users list
```
This will list all users in a table.
```
python gig_client.py http://localhost:8000/ users list --json
```
This will list all users but in a JSON format.

```
python gig_client.py http://localhost:8000/ users postings retrieve --pk 2
```
This will display posting with id=2.

When using either `create`, `update`, `filter`, the user will be prompted to input data by field.\
The action will be perfomed once all required data is inserted.\
In the case of creating new user, a token string will be returned and a .token file created.\
Example:
```
python gig_client.py http://127.0.0.1:8000/ users create
```
The outpur will be:
```
'Please input necessary data:'
first_name:
last_name:
email:
phone_number:
address:
```
Expected output:
```
{'Token': '<token-string>'}
```
