# source:
# https://docs.djangoproject.com/en/5.0/topics/testing/advanced/#integration-with-coverage-py

coverage run --source='.' manage.py test tests
coverage report -m
