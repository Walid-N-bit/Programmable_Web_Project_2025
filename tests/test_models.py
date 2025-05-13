"""
Populate the database with sample data for testing purposes.
"""

import os
from datetime import datetime, timedelta

import django
from django.test import TestCase

from gigwork.models import Gig, Posting, User

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()


class GigworkTests(TestCase):
    """
    Test the Gigwork models.
    """

    def setUp(self):
        # Create necessary datetime objects
        week_ago = datetime.now().date() - timedelta(days=7)
        week_ahead = datetime.now().date() + timedelta(days=7)
        now = datetime.now().date()

        # Create Customers
        user1 = User.objects.create(
            first_name="User One",
            last_name="User One",
            email="customer1@asd.com",
            phone_number="1234567890",
            address="Testitie 12, 90500 Oulu",
        )
        user2 = User.objects.create(
            first_name="User Two",
            last_name="User Two",
            email="customer2@asd.com",
            phone_number="0987654321",
            address="Testitie 13, 90520 Oulu",
        )

        # Create Employees
        user3 = User.objects.create(
            first_name="User three",
            last_name="user three",
            email="employee1@asd.com",
            phone_number="1234567890",
        )
        User.objects.create(
            first_name="user four",
            last_name="user four",
            email="employee2@asd.com",
            phone_number="0987654321",
        )

        # Create Postings
        Posting.objects.create(
            title="Posting One",
            description="Hey you, you're finally awake.",
            owner=user1,
            expires_at=week_ahead,
            price=100.00,
            status="open",
        )
        posting2 = Posting.objects.create(
            title="Posting Two",
            description="You were trying to cross the border, right?",
            owner=user2,
            expires_at=week_ago,
            price=200.00,
            status="expired",
        )
        posting3 = Posting.objects.create(
            title="Posting Three",
            description="Walked right into that Imperial ambush, same as us and that thief there.",
            owner=user3,
            expires_at=week_ahead,
            price=300.00,
            status="accepted",
        )

        # Create Gigs
        Gig.objects.create(
            owner=user1,
            posting=posting2,
            start_date=week_ago,
            end_date=now,
            status="completed",
        )
        Gig.objects.create(
            owner=user2,
            posting=posting3,
            start_date=week_ago,
            end_date=week_ahead,
            status="in_progress",
        )

    def test_user_count(self):
        users = User.objects.all()
        self.assertEqual(users.count(), 4)

    def test_posting_count(self):
        postings = Posting.objects.all()
        self.assertEqual(postings.count(), 3)

    def test_gig_count(self):
        gigs = Gig.objects.all()
        self.assertEqual(gigs.count(), 2)

    def test__str__(self):
        self.assertEqual(str(User.objects.get(id=1)), "User One User One")
        self.assertEqual(str(Posting.objects.get(id=1)), "Posting One")
        self.assertEqual(str(Gig.objects.get(id=1)), "Posting Two")
