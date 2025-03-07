"""
This module contains viewsets for the API. Viewsets in Django are called "resources"
in other frameworks. They provide actions to execute GEt, POST, PUT, DELETE, PATCH requests.

Sources:
https://www.django-rest-framework.org/tutorial/quickstart/#views
https://www.django-rest-framework.org/api-guide/exceptions/#apiexception
https://lovelace.oulu.fi/ohjelmoitava-web/ohjelmoitava-web/implementing-rest-apis-with-flask/#dynamic-schemas-static-methods

"""
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import UnsupportedMediaType, ParseError
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse
from jsonschema import validate, ValidationError
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

    @staticmethod
    def json_schema():
        schema = {
            "type":"object",
            "required":["first_name", "last_name", "email"],
            "properties":{
                "first_name":{
                    "type":"string"
                },
                "last_name":{
                    "type":"string"
                },
                "email":{
                    "type":"string"
                },
                "phone_number":{
                    "type":"string"
                },
                "address":{
                    "type":"string"
                },
                "role":{
                    "type":"string"
                }
            }
        }
        return schema
    def get_permissions(self):
        """
        The purpose of this method is to allow for creating new users without
        being blocked by the authentication and permission schemes.
        """
        if self.action == 'new_user':
            permission_classes = []
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    authentication_classes = [TokenAuthentication]

    @action(detail=False, methods=['post'])
    def new_user(self, request):
        """
        create new user, return authentication token for that user.
        data is sent from the client in json format, required fields are: first_name,
        last_name, email.
        """
        if request.content_type is not 'application/json':
            raise UnsupportedMediaType
        try:
            validate(request.data, UserViewSet.json_schema())
        except ValidationError as e:
            raise ParseError(detail=str(e))
        
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({"Token": token.key}, status=status.HTTP_201_CREATED) 

    @action(detail=False, methods=['get'])
    def filter_users(self, request):
        """
        query users by fields. e.g: /filter_users/?first_name=John&role=customer
        """
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address', 'role']
        user_list = FilterByField(request, fields, User.objects.all())
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
    """authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]"""
    authentication_classes = []
    permission_classes = []

    @staticmethod
    def json_schema():
        schema = {
            "type":"object",
            "required":["title", "description", "price"],
            "properties":{
                "title":{
                    "type":"string"
                },
                "description":{
                    "type":"string"
                },
                "user":{
                    "type":"number"
                },
                "start_date":{
                    "type":"string"
                },
                "end_date":{
                    "type":"string"
                },
                "price":{
                    "type":"number"
                },
                "status":{
                    "type":"string"
                },
            }
        }
        return schema
    
    def list(self, request):
        all_gigs = Gig.objects.all()
        serializer = GigSerializer(all_gigs, many=True)
        return JsonResponse(serializer.data, safe=False)
        
    def create(self, request):
        if request.content_type is not 'application/json':
            raise UnsupportedMediaType
        try:            
            validate(request.data, GigViewSet.json_schema())
        except ValidationError as e:
            print(f"Validation Error: {e.message}")
            raise ParseError(detail=f"{e.message}")
        
        serializer = GigSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"result":"gig added successfully."}, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return JsonResponse({"result":"Data not valid"}, status=status.HTTP_400_BAD_REQUEST)
        
    def update(self, request, pk=None):
        try:            
            validate(request.data, GigViewSet.json_schema())
        except ValidationError as e:
            print(f"Validation Error: {e.message}")
            raise ParseError(detail=f"{e.message}")
        
        gig = self.get_object()
        serializer = GigSerializer(gig, data= request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"result":"gig updated"}, status=status.HTTP_200_OK)
        else:
            print(serializer.errors)
            return JsonResponse({"result":"Data not valid"}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['get'])
    def filter_gigs(self, request):
        """
        query gigs by fields
        """
        fields = ['title', 'description', 'user', 'start_date', 'end_date', 'price', 'status']
        gig_list = FilterByField(request, fields, Gig.objects.all())
        serialized = GigSerializer(gig_list, many=True)
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
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [permissions.IsAuthenticated]
    authentication_classes = []
    permission_classes = []

    @staticmethod
    def json_schema():
        schema = {
            "type":"object",
            "required":["title", "description", "price"],
            "properties":{
                "title":{
                    "type":"string"
                },
                "description":{
                    "type":"string"
                },
                "user":{
                    "type":"number"
                },
                "created_at":{
                    "type":"string"
                },
                "expires_at":{
                    "type":"string"
                },
                "price":{
                    "type":"number"
                },
                "status":{
                    "type":"string"
                },
            }
        }
        return schema

    def create(self, request):
        if request.content_type is not 'application/json':
            raise UnsupportedMediaType
        try:            
            validate(request.data, PostingViewSet.json_schema())
        except ValidationError as e:
            print(f"Validation Error: {e.message}")
            raise ParseError(detail=f"{e.message}")
        
        serializer = PostingSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({}, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)
        
    def update(self, request, pk=None):
        try:            
            validate(request.data, PostingViewSet.json_schema())
        except ValidationError as e:
            print(f"Validation Error: {e.message}")
            raise ParseError(detail=f"{e.message}")
        
        posting = self.get_object()
        serializer = PostingSerializer(posting, data= request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({}, status=status.HTTP_200_OK)
        else:
            print(serializer.errors)
            return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['get'])
    def filter_postings(self, request):
        """
        query postings by fields
        """
        fields = ['title', 'description', 'user', 'created_at', 'expires_at', 'price', 'status']
        posting_list = FilterByField(request, fields, Posting.objects.all())
        serialized = PostingSerializer(posting_list, many=True)
        return JsonResponse(serialized.data, safe=False)

def FilterByField(request, fields, filter_list):
    """
    this function filters a list using every field in the query paramters and returns a list that
    satisfies the query parameters provided.
    """
    for field in fields:
        value = request.query_params.get(field)
        if value is not None:
            kwags = {field: value}
            filter_list = filter_list.filter(**kwags)
    return filter_list
