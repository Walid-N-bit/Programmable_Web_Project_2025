import os
import django
# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")  
django.setup()

from gigwork.models import User, Posting, Gig
from datetime import datetime, timedelta



def populate_db():
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
    user4 = User.objects.create(
        first_name="Alphonse",
        last_name="Elric",
        email="employee2@asd.com",
        phone_number="0987654321",
        role="employee",
    )

    # Create Postings
    posting1 = Posting.objects.create(
        title="Posting One",
        description="Hey you, you're finally awake.",
        user=user1,
        expires_at=week_ahead,
        price=100.00,
        status="open",
    )
    posting2 = Posting.objects.create(
        title="Posting Two",
        description="You were trying to cross the border, right?",
        user=user2,
        expires_at=week_ago,
        price=200.00,
        status="expired",
    )
    posting3 = Posting.objects.create(
        title="Posting Three",
        description="Walked right into that Imperial ambush, same as us, and that thief over there.",
        user=user3,
        expires_at=week_ahead,
        price=300.00,
        status="accepted",
    )

    # Create Gigs
    gig1 = Gig.objects.create(
        title="Gig One",
        description="For the Emperor!",
        user=user1,
        start_date=week_ago,
        end_date=now,
        price=100.00,
        status="completed",
    )
    gig2 = Gig.objects.create(
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
