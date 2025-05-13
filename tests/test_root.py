"""
Sources:
https://docs.djangoproject.com/en/5.1/topics/testing/overview/
https://www.django-rest-framework.org/api-guide/testing/#api-test-cases
"""

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django

django.setup()

from rest_framework.test import APITestCase, APIClient
from rest_framework import status


class APIRootTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        return super().setUp()

    def test_api_root_view(self):
        url = "/gigwork/api/root/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.status_code)
