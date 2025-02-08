from datetime import datetime, timedelta
from django.test import TestCase
from gigwork.models import Gig, Employee, Customer, Posting


class GigworkTests(TestCase):

    def setUp(self):
        # Create necessary datetime objects
        week_ago = datetime.now().date() - timedelta(days=7)
        week_ahead = datetime.now().date() + timedelta(days=7)
        now = datetime.now().date()
                
        # Create Customers
        customer1 = Customer.objects.create(
            first_name="Customer One",
            last_name="Customer One",
            email="customer1@asd.com",
            phone_number="1234567890",
            address="Testitie 12, 90500 Oulu",
        )
        customer2 = Customer.objects.create(
            first_name="Customer Two",
            last_name="Customer Two",
            email="customer2@asd.com",
            phone_number="0987654321",
            address="Testitie 13, 90520 Oulu",
        )

        # Create Employees
        employee1 = Employee.objects.create(
            first_name="Employee One",
            last_name="Employee One",
            email="employee1@asd.com",
            phone_number="1234567890",
        )
        employee2 = Employee.objects.create(
            first_name="Employee Two",
            last_name="Employee Two",
            email="employee2@asd.com",
            phone_number="0987654321",
        )

        # Create Postings
        posting1 = Posting.objects.create(
            title="Posting One",
            description="Hey you, you're finally awake.",
            customer=customer1,
            expires_at=week_ahead,
            price=100.00,
            status="open",
        )
        posting2 = Posting.objects.create(
            title="Posting Two",
            description="You were trying to cross the border, right?",
            customer=customer2,
            expires_at=week_ago,
            price=200.00,
            status="expired",
        )
        posting3 = Posting.objects.create(
            title="Posting Three",
            description="Walked right into that Imperial ambush, same as us, and that thief over there.",
            customer=customer1,
            expires_at=week_ahead,
            price=300.00,
            status="accepted",
        )

        # Create Gigs
        gig1 = Gig.objects.create(
            title="Gig One",
            description="For the Emperor!",
            customer=customer1,
            employee=employee1,
            start_date=week_ago,
            end_date=now,
            price=100.00,
            status="completed",
        )
        gig2 = Gig.objects.create(
            title="Gig Two",
            description="Damn you Stormcloaks. Skyrim was fine until you came along.",
            customer=customer2,
            employee=employee2,
            start_date=week_ago,
            end_date=week_ahead,
            price=200.00,
            status="in_progress",
        )

    def test_customer_count(self):
        customers = Customer.objects.all()
        self.assertEqual(customers.count(), 2)

    def test_employee_count(self):
        employees = Employee.objects.all()
        self.assertEqual(employees.count(), 2)

    def test_posting_count(self):
        postings = Posting.objects.all()
        self.assertEqual(postings.count(), 3)

    def test_gig_count(self):
        gigs = Gig.objects.all()
        self.assertEqual(gigs.count(), 2)
