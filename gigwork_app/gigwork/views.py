from django.shortcuts import render

from gigwork.models import Employee, Customer, Gig, Posting
from rest_framework import permissions, viewsets

from gigwork.serializers import CustomerSerializer, EmployeeSerializer, GigSerializer, PostingSerializer

class CustomerViewSet(viewsets.ModelViewSet):           #API endpoint to view and edit customers
    queryset = Customer.objects.all().order_by('last_name')
    serializer_class = CustomerSerializer
    #permission_classes = [permissions.IsAuthenticated]

class EmployeeViewSet(viewsets.ModelViewSet):           #API endpoint to view and edit employees
    queryset = Employee.objects.all().order_by('last_name')
    serializer_class = EmployeeSerializer
    #permission_classes = [permissions.IsAuthenticated]

class GigViewSet(viewsets.ModelViewSet):                #API endpoint to view and edit gigs
    queryset = Gig.objects.all().order_by('status')
    serializer_class = GigSerializer

class PostingViewSet(viewsets.ModelViewSet):            #API endpoint to view and edit postings
    queryset = Posting.objects.all().order_by('status')
    serializer_class = PostingSerializer
