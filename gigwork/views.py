"""
This module contains viewsets for the API. Viewsets in Django are called "resources"
in other frameworks. They provide actions to execute GEt, POST, PUT, DELETE, PATCH requests. 
"""
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token

from django.http import JsonResponse

from gigwork.serializers import UserSerializer, GigSerializer, PostingSerializer
from gigwork.models import User, Gig, Posting

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint to view and edit users
    this viewset provides default actions inherited from 'ModelViewSet', 
    theses are: 'list', 'create', 'destroy', 'retrieve', 'update'.
    the viewset also provides two custom actions. These are:
    'new_user', 'filter_users'
    """
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'new_user':
            permission_classes = []
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    authentication_classes = [TokenAuthentication]

    @action(detail=False, methods=['post'])
    def new_user(self, request):
        """
        create new user, return authentication token for that user
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        return JsonResponse({"Token": token.key}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def filter_users(self, request):
        """
        query users by fields
        """
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address', 'role']
        user_list = User.objects.all()
        for field in fields:
            f = request.query_params.get(field)
            if f is not None:
                kwags = {field: f}
                user_list = user_list.filter(**kwags)
        serialized = UserSerializer(user_list, many=True)
        return JsonResponse(serialized.data, safe=False)

class GigViewSet(viewsets.ModelViewSet):
    """
    API endpoint to view and edit gigs
    this viewset provides default actions inherited from 'ModelViewset', 
    theses are: 'list', 'create', 'destroy', 'retrieve', 'update'.
    the viewset also provides a custom action:
    'filter_gigs': allows for querying gigs by fields.
    """
    queryset = Gig.objects.all().order_by('status')
    serializer_class = GigSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    @action(detail=False, methods=['get'])
    def filter_gigs(self, request):
        """
        query gigs by fields
        """
        fields = ['title', 'description', 'user', 'start_date', 'end_date', 'price', 'status']
        gig_list = Gig.objects.all()
        for field in fields:
            f = request.query_params.get(field)
            if f is not None:
                kwags = {field: f}
                gig_list = gig_list.filter(**kwags)
        serialized = UserSerializer(gig_list, many=True)
        return JsonResponse(serialized.data, safe=False)

class PostingViewSet(viewsets.ModelViewSet):
    """
    API endpoint to view and edit postings
    this viewset provides default actions inherited from 'ModelViewset', 
    theses are: 'list', 'create', 'destroy', 'retrieve', 'update'.
    the viewset also provides a custom action:
    'filter_postings': allows for querying postings by fields.
    """
    queryset = Posting.objects.all().order_by('status')
    serializer_class = PostingSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    @action(detail=False, methods=['get'])
    def filter_postings(self, request):
        """
        query postings by fields
        """
        fields = ['title', 'description', 'user', 'created_at', 'expires_at', 'price', 'status']
        posting_list = Gig.objects.all()
        for field in fields:
            f = request.query_params.get(field)
            if f is not None:
                kwags = {field: f}
                posting_list = posting_list.filter(**kwags)
        serialized = UserSerializer(posting_list, many=True)
        return JsonResponse(serialized.data, safe=False)
