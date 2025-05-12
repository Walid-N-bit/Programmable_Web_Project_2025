"""
Sources:
https://docs.djangoproject.com/en/5.1/topics/testing/overview/
https://www.django-rest-framework.org/api-guide/testing/#api-test-cases
"""

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from datetime import datetime, timedelta
from rest_framework.test import APITestCase, APIClient, force_authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from gigwork.views import Posting, User

class PostingTests(APITestCase):
  def setUp(self):
    self.client = APIClient()
    self.user = User.objects.create(first_name='first_name', last_name='last_name', email="test@mail.com")

    self.posting = Posting.objects.create(
                                  title="title",
                                  description="This is a description for the test posting",
                                  expires_at=datetime.now().date() + timedelta(days=7),
                                  price=100.00,
                                  status="open",
                                  owner=self.user
                                  )
    self.client.force_authenticate(user=self.user)
    return super().setUp()
    
  def test_postings_list(self):
    url = "/gigwork/api/postings/"
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    print(response.status_code)

  def test_postings_retrieve(self):
    url = f"/gigwork/api/postings/{self.posting.id}/"
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    print(response.status_code)

  def test_postings_filter(self):
    url = "/gigwork/api/postings/?price=100.00&status=accepted"
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    print(response.status_code)
  
  def test_postings_create(self):
    url = "/gigwork/api/postings/"
    end_date=datetime.now().date() + timedelta(days=7)
    data = {
            "title": "postest",
            "description": "This is a description",
            "expires_at": end_date,
            "price": 100.00,
            "status": "open",
            }

    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    print(response.status_code)

  def test_postings_update(self):
    url = f"/gigwork/api/postings/{self.posting.id}/"
    end_date=datetime.now().date() + timedelta(days=7)
    data = {
            "title": "postest2",
            "description": "This is a description 2",
            "expires_at": end_date,
            "price": 100.00,
            "status": "accepted",
            }

    response = self.client.put(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    print(response.status_code)

  def test_postings_destroy(self):
    url = f"/gigwork/api/postings/{self.posting.id}/"
    response = self.client.delete(url)
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    print(response.status_code)
  
  def test_posting_parse_error(self):
    url = "/gigwork/api/postings/"
    data = {
            "title": "postest2",
            "description": "This is a description 2",
            }
    response = self.client.post(url, data, format='json')
    print(response.status_code)
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

  def test_posting_unsupportedmediatype(self):
    url = "/gigwork/api/postings/"
    data = {
            "title": "postest2",
            "description": "This is a description 2",
            "price": 100.00,
            "status": "open",
            }
    response = self.client.post(url, data, content_type='application/xml')
    print(response.status_code)
    self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

  def test_postings_negative_price(self):
    url = "/gigwork/api/postings/"
    end_date=datetime.now().date() + timedelta(days=7)
    data = {
            "title": "postest",
            "description": "This is a description",
            "expires_at": end_date,
            "price": -100.00,
            "status": "open",
            }
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    print(response.status_code)

  def test_postings_non_number_price(self):
    url = "/gigwork/api/postings/"
    end_date=datetime.now().date() + timedelta(days=7)
    data = {
            "title": "postest",
            "description": "This is a description",
            "expires_at": end_date,
            "price": "one hundred euros",
            "status": "open",
            }
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    print(response.status_code)
