"""
This script prints the token for the first user in the database.
"""

import os

import django
from rest_framework.authtoken.models import Token

from gigwork.models import User

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

for user in User.objects.all():
    token = Token.objects.get(user=user)
    if token is not None:
        break
print("Token ", token.key)
