from django.db import models
from django.conf import settings

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    role = models.CharField(max_length=10, 
                            choices=[
        ('customer','Customer'), ('employee', 'Employee')
        ]
        )
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Gig(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        default=0  # Assuming user with ID 1 exists
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("in_progress", "In Progress"),
            ("completed", "Completed"),
        ],
    )

    def __str__(self):
        return self.title

class Posting(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        default=0  # Assuming user with ID 1 exists
    )
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[("open", "Open"), ("expired", "Expired"), ("accepted", "Accepted")],
    )

    def __str__(self):
        return self.title
