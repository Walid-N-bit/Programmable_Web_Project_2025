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
For testing just installing Django is enough:\
```
python -m venv .testenv
source .testenv/bin/activate
pip install Django
```
A script populating the database is included in .../gigwork_app/gigwork_app/populatedb.py:
```
cd gigwork_app
python manage.py makemigrations
python manage.py migrate
python manage.py shell < populatedb.py
```
This creates a file called db.sqlite3 that contains the db.\
Due to time constraints of other courses, there was no time to implement the DB in a proper framework, but this is definitely something that could still be done.
