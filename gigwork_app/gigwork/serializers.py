from gigwork.models import Employee, Customer, Gig, Posting
from rest_framework import serializers

class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address']

class EmployeeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'email', 'phone_number']

class GigSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Gig
        fields = ['title', 'description', 'customer', 'employee', 'start_date', 
                  'end_date', 'price', 'status']

class PostingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Posting
        fields = ['title', 'description', 'customer', 'employee', 'created_at', 
                  'expires_at', 'price', 'status']
