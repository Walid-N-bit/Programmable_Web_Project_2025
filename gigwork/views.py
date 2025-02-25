from django.shortcuts import render

from gigwork.models import User, Gig, Posting
from rest_framework import permissions, viewsets

from gigwork.serializers import UserSerializer, GigSerializer, PostingSerializer

class UserViewSet(viewsets.ModelViewSet):           #API endpoint to view and edit users
    queryset = User.objects.all().order_by('last_name')
    serializer_class = UserSerializer
    #permission_classes = [permissions.IsAuthenticated]


class GigViewSet(viewsets.ModelViewSet):                #API endpoint to view and edit gigs
    queryset = Gig.objects.all().order_by('status')
    serializer_class = GigSerializer

class PostingViewSet(viewsets.ModelViewSet):            #API endpoint to view and edit postings
    queryset = Posting.objects.all().order_by('status')
    serializer_class = PostingSerializer
