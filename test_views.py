import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from rest_framework.test import APIClient, force_authenticate
from gigwork.models import User

c = APIClient()
user = {
    "first_name": "Luke",
    "last_name": "Skywalker",
    "email": "258@jedi.com",
    "phone_number": "5555558765",
    "address": "Tatooine, Outer Rim Territories",
    "role": "employee"
  }
response = c.post('/gigwork/api/users/new_user/', user, content_type='application/json')

print(response.status_code)

