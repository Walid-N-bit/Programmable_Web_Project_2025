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
from gigwork.views import Gig, User

class GigTests(APITestCase):
  def setUp(self):
    self.client = APIClient()
    self.user = User.objects.create(first_name='first_name', last_name='last_name', email="test@mail.com")
    self.gig = Gig.objects.create(
                                  title="testgig",
                                  description="This is a description for the test gig",
                                  user=self.user,
                                  start_date=datetime.now().date() - timedelta(days=7),
                                  end_date=datetime.now().date() + timedelta(days=7),
                                  price=100.00,
                                  status="in_progress"
                                  )
    self.client.force_authenticate(user=self.user)
    return super().setUp()
    
  def test_gigs(self):
    url = "/gigwork/api/gigs/"
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    print(response.status_code)

  def test_filter_gigs(self):
    url = "/gigwork/api/gigs/filter_gigs/?price=100.00&status=in_progress"
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    print(response.status_code)
  
  def test_gigs_create(self):
    url = "/gigwork/api/gigs/"
    data = {
            "title": "newgig",
            "description": "This is a new gig",
            "start_date":"2025-02-21T00:00:00",
            "end_date": "2025-02-28T00:00:00",
            "price": 100.00,
            "status": "pending",
            "user":self.user.id,
            }
    response = self.client.post(url, data, format='json')
    print(response.status_code)
    #print(response.content)
    #print(response)
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)

  def test_gigs_update(self):
    url = f"/gigwork/api/gigs/{self.gig.id}/"
    start_date=datetime.now().date() - timedelta(days=7)
    end_date=datetime.now().date() + timedelta(days=7)
    data = {
            "title": "testgig2",
            "description": "This is a description 2",
            "start_date":start_date,
            "end_date": end_date,
            "price": 100.00,
            "status": "completed",
            "user":self.user.id,
            }

    response = self.client.put(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    print(response.status_code)

  def test_gigs_destroy(self):
    url = f"/gigwork/api/gigs/{self.gig.id}/"
    response = self.client.delete(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    print(response.status_code)
    