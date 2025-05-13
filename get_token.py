import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django

django.setup()

from rest_framework.authtoken.models import Token

from gigwork.models import User

for user in User.objects.all():
    token = Token.objects.get(user=user)
    if token is not None:
        break
print("Token ", token.key)
