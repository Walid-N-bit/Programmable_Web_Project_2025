"""
Sources:
https://docs.djangoproject.com/en/5.1/topics/testing/overview/
https://www.django-rest-framework.org/api-guide/testing/#api-test-cases
"""

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

import json
from rest_framework.test import APITestCase, APIClient, force_authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from gigwork.views import User

class UserTests(APITestCase):
  def setUp(self):
    self.client = APIClient()
    self.user = User.objects.create(first_name='first_name', last_name='last_name', email="test@mail.com")
    self.client.force_authenticate(user=self.user)
    return super().setUp()
  
  def test_users_create(self):
    url = "/gigwork/api/users/"
    data = {"first_name":"new_fn", "last_name":"new_ln", "email":"new@testmail.com"}
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    print(response.status_code)
  
  def test_users_list(self):
    url = "/gigwork/api/users/"
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    print(response.status_code)

  def test_users_retrieve(self):
    url = f"/gigwork/api/users/{self.user.id}/"
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    print(response.status_code)

  def test_users_filter(self):
    url = "/gigwork/api/users/?first_name=first_name&last_name=last_name&email=test@mail.com"
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    print(response.status_code)
  
  def test_users_update(self):
    url = f"/gigwork/api/users/{self.user.id}/"
    data = {"first_name":"new_fn2", "last_name":"new_ln2", "email":"new2@testmail.com"}
    response = self.client.put(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    print(response.status_code)

  def test_users_destroy(self):
    url = f"/gigwork/api/users/{self.user.id}/"
    response = self.client.delete(url)
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    print(response.status_code)

  def test_create_parse_error(self):
    url = "/gigwork/api/users/"
    data = {"first_name":"new_fn","last_name":"new_ln"}
    response = self.client.post(url, data, content_type='application/json')
    print(response.status_code)
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

  def test_update_parse_error(self):
    url = f"/gigwork/api/users/{self.user.id}/"
    data = {"first_name":"new_fn", "email":"new@testmail.com"}
    response = self.client.put(url, data, content_type='application/json')
    print(response.status_code)
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

  def test_user_create_unsupportedmediatype(self):
    url = "/gigwork/api/users/"
    data = '{"first_name":"mm", "last_name":"new_ln2", "email":"new@testmail.com"}'
    response = self.client.post(url, data, content_type='application/xml')
    print(response.status_code)
    self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
  
  def test_user_update_unsupportedmediatype(self):
    url = f"/gigwork/api/users/{self.user.id}/"
    data = '{"first_name":"different_fn", "last_name":"last_name", "email":"new@testmail.com"}'
    response = self.client.put(url, data, content_type='application/xml')
    print(response.status_code)
    self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
  