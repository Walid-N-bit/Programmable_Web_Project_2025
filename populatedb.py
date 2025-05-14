"""
This script populates the database with sample data for testing purposes.
"""

import os
from datetime import datetime, timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django  # pylint: disable=wrong-import-position

django.setup()

from gigwork.models import (Gig,  # pylint: disable=wrong-import-position
                            Posting, User)


def populate_db():
    """
    Populate the database with sample data for testing purposes.
    """
    # Create necessary datetime objects
    week_ago = datetime.now().date() - timedelta(days=7)
    week_ahead = datetime.now().date() + timedelta(days=7)
    now = datetime.now().date()

    # Create Customers
    user1 = User.objects.create(
        first_name="John",
        last_name="Wick",
        email="customer1@asd.com",
        phone_number="1234567890",
        address="Testitie 12, 90500 Oulu",
        role="customer",
    )
    user2 = User.objects.create(
        first_name="John",
        last_name="117",
        email="customer2@asd.com",
        phone_number="0987654321",
        address="Testitie 13, 90520 Oulu",
        role="customer",
    )

    # Create Employees
    user3 = User.objects.create(
        first_name="Edward",
        last_name="Elric",
        email="employee1@asd.com",
        phone_number="1234567890",
        role="employee",
    )
    User.objects.create(
        first_name="Alphonse",
        last_name="Elric",
        email="employee2@asd.com",
        phone_number="0987654321",
        role="employee",
    )

    # Create Postings
    Posting.objects.create(
        title="Posting One",
        description="Hey you, you're finally awake.",
        user=user1,
        expires_at=week_ahead,
        price=100.00,
        status="open",
    )
    Posting.objects.create(
        title="Posting Two",
        description="You were trying to cross the border, right?",
        user=user2,
        expires_at=week_ago,  # pylint: disable=duplicate-code
        price=200.00,
        status="expired",
    )
    Posting.objects.create(
        title="Posting Three",
        description="Walked right into that Imperial ambush, same as us, and that thief there.",
        user=user3,
        expires_at=week_ahead,
        price=300.00,
        status="accepted",
    )

    # Create Gigs
    Gig.objects.create(
        title="Gig One",
        description="For the Emperor!",
        user=user1,
        start_date=week_ago,
        end_date=now,
        price=100.00,
        status="completed",
    )
    Gig.objects.create(
        title="Gig Two",
        description="Damn you Stormcloaks. Skyrim was fine until you came along.",
        user=user2,
        start_date=week_ago,
        end_date=week_ahead,
        price=200.00,
        status="in_progress",
    )


populate_db()
print("Database populated successfully.")
