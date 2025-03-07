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
                                  title="postesting",
                                  description="This is a description for the test posting",
                                  user=self.user,
                                  expires_at=datetime.now().date() + timedelta(days=7),
                                  price=100.00,
                                  status="accepted"
                                  )
    self.client.force_authenticate(user=self.user)
    return super().setUp()
    
  def test_postings(self):
    url = "/gigwork/api/postings/"
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    print(response.status_code)

  def test_filter_postings(self):
    url = "/gigwork/api/postings/filter_postings/?price=100.00&status=accepted"
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    print(response.status_code)
  
  def test_posting_create(self):
    url = f"/gigwork/api/postings/{self.posting.id}/"
    end_date=datetime.now().date() + timedelta(days=7)
    data = {
            "title": "postest",
            "description": "This is a description",
            "expires_at": end_date,
            "price": 100.00,
            "status": "accepted",
            "user":self.user.id,
            }

    response = self.client.put(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    print(response.status_code)

  def test_posting_update(self):
    url = f"/gigwork/api/postings/{self.posting.id}/"
    end_date=datetime.now().date() + timedelta(days=7)
    data = {
            "title": "postest2",
            "description": "This is a description 2",
            "expires_at": end_date,
            "price": 100.00,
            "status": "accepted",
            "user":self.user.id,
            }

    response = self.client.put(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    print(response.status_code)

  def test_posting_destroy(self):
    url = f"/gigwork/api/postings/{self.posting.id}/"
    response = self.client.delete(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    print(response.status_code)
    