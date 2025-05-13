"""
Sources:
https://docs.djangoproject.com/en/5.1/topics/testing/overview/
https://www.django-rest-framework.org/api-guide/testing/#api-test-cases
"""

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django

django.setup()

from datetime import datetime, timedelta

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from gigwork.views import Gig, Posting, User


class GigTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create(
            first_name="first_name1", last_name="last_name1", email="test1@mail.com"
        )
        self.user2 = User.objects.create(
            first_name="first_name2", last_name="last_name2", email="test2@mail.com"
        )
        self.posting = Posting.objects.create(
            title="title",
            description="This is a description for the test posting",
            expires_at=datetime.now().date() + timedelta(days=7),
            price=100.00,
            status="open",
            owner=self.user1,
        )
        self.gig = Gig.objects.create(
            owner=self.user2,
            posting=self.posting,
            start_date=datetime.now().date() - timedelta(days=7),
            end_date=datetime.now().date() + timedelta(days=7),
            status="in_progress",
        )
        self.client.force_authenticate(user=self.user2)
        return super().setUp()

    def test_gigs_list(self):
        url = "/gigwork/api/gigs/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.status_code)

    def test_gigs_retrieve(self):
        url = f"/gigwork/api/gigs/{self.gig.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.status_code)

    def test_gigs_filter(self):
        url = "/gigwork/api/gigs/?price=100.00&status=in_progress"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.status_code)

    def test_gigs_create(self):
        url = "/gigwork/api/gigs/"
        new_posting = Posting.objects.create(
            title="title",
            description="This is a description for the test posting",
            expires_at=datetime.now().date() + timedelta(days=7),
            price=100.00,
            status="open",
            owner=self.user1,
        )
        data = {
            "posting": new_posting.id,
            "status": "pending",
        }
        response = self.client.post(url, data, format="json")
        print(response.status_code)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_gigs_update(self):
        url = f"/gigwork/api/gigs/{self.gig.id}/"
        data = {
            "posting": self.posting.id,
            "status": "completed",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.status_code)

    def test_gigs_destroy(self):
        url = f"/gigwork/api/gigs/{self.gig.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        print(response.status_code)
