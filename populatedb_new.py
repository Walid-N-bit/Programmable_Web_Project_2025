"""
Populate the database with sample data for testing purposes.
"""

import os
from datetime import datetime, timedelta

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()

from gigwork.models import Gig, Posting, User


def populate_db():
    """
    Populate the database with sample data for testing purposes.
    """
    week_ago = datetime.now() - timedelta(days=7)
    week_ahead = datetime.now() + timedelta(days=7)
    now = datetime.now()

    # Create Users (Pop Culture, excluding Star Wars)
    users = [
        {"first_name": "Tony", "last_name": "Stark", "email": "tony@stark.com"},
        {"first_name": "Bruce", "last_name": "Wayne", "email": "bruce@wayne.com"},
        {"first_name": "Clark", "last_name": "Kent", "email": "clark@kent.com"},
        {"first_name": "Diana", "last_name": "Prince", "email": "diana@amazon.com"},
        {"first_name": "Peter", "last_name": "Parker", "email": "peter@dailybugle.com"},
        {"first_name": "Wanda", "last_name": "Maximoff", "email": "wanda@scarlet.com"},
    ]

    user_objs = []
    for u in users:
        user = User.objects.create(
            first_name=u["first_name"],
            last_name=u["last_name"],
            email=u["email"],
            phone_number="0000000000",
            address="123 Fictional St",
        )
        user_objs.append(user)

    # Create Postings
    posting1 = Posting.objects.create(
        title="Help with yard work",
        description="Trim bushes, mow lawn, 2-3 hours",
        owner=user_objs[0],  # Tony Stark
        expires_at=week_ahead,
        price=120.00,
        status="open",
    )

    posting2 = Posting.objects.create(
        title="Assemble furniture",
        description="IKEA wardrobe assembly",
        owner=user_objs[1],  # Bruce Wayne
        expires_at=week_ago,
        price=90.00,
        status="expired",
    )

    # Create Gigs
    Gig.objects.create(
        owner=user_objs[2],  # Clark Kent
        posting=posting1,
        start_date=week_ago,
        end_date=now,
        status="completed",
    )  # pylint: disable=duplicate-code

    Gig.objects.create(
        owner=user_objs[3],  # Diana Prince
        posting=posting2,
        start_date=week_ago,
        end_date=week_ahead,
        status="in_progress",
    )

    print("Database populated successfully.")


populate_db()
