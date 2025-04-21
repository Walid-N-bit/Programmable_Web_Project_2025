"""
This module contains viewsets for the API. Viewsets in Django are called "resources"
in other frameworks. They provide actions to execute GEt, POST, PUT, DELETE, PATCH requests.

Sources:
https://www.django-rest-framework.org/tutorial/quickstart/#views
https://www.django-rest-framework.org/api-guide/exceptions/#apiexception
https://lovelace.oulu.fi/ohjelmoitava-web/ohjelmoitava-web/implementing-rest-apis-with-flask/#dynamic-schemas-static-methods
https://www.django-rest-framework.org/api-guide/caching/
"""
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions, viewsets, status
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import UnsupportedMediaType, ParseError
#from rest_framework.response import Response
from django.http import JsonResponse
from jsonschema import validate, ValidationError
from gigwork.serializers import UserSerializer, GigSerializer, PostingSerializer
from gigwork.models import User, Gig, Posting

class JsonSchemaMixin:
    def create(self, request):
        try:
            validate(request.data, self.json_schema())
            return super().create(request)
        except ValidationError as e:
            raise ParseError(detail=str(e))

    def update(self, request):
        if request.content_type != 'application/json':
            raise UnsupportedMediaType
        try:
            validate(request.data, self.json_schema())
            return super().update(request)
        except ValidationError as e:
            raise ParseError(detail=str(e))

class UserViewSet(JsonSchemaMixin, viewsets.ModelViewSet):
    """
    API endpoint to view and edit users
    this viewset provides default actions inherited from 'ModelViewSet',
    theses are: 'list', 'create', 'destroy', 'retrieve', 'update'.
    the viewset also provides two custom actions. These are:
    'new_user', 'filter_users'
    """
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    filterset_fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'address', 'role']
    renderer_classes = [JSONRenderer]
    parser_classes = [JSONParser]

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
    #def get_permissions(self):
    #    pass
    #    """
    #    The purpose of this method is to allow for creating new users without
    #    being blocked by the authentication and permission schemes.
    #    """
    #    if self.action == 'new_user':
    #        permission_classes = []
    #    else:
    #        permission_classes = [permissions.IsAuthenticated]
    #    return [permission() for permission in permission_classes]
    #authentication_classes = [TokenAuthentication]
    permission_classes = []
    authentication_classes = []

    @method_decorator(cache_page(60 * 60))
    @method_decorator(vary_on_headers("Authorization"))
    def list(self, request):
        return super().list(request)

    @method_decorator(cache_page(60 * 60))
    @method_decorator(vary_on_headers("Authorization"))
    def retrieve(self, request, pk=None):
        return super().retrieve(request, pk=None)

    def create(self, request):
        """
        create new user, return authentication token for that user.
        data is sent from the client in json format, required fields are: first_name,
        last_name, email.
        """
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.create(user=user)
        return JsonResponse({"Token": token.key}, status=status.HTTP_201_CREATED)

class PostingViewSet(JsonSchemaMixin, viewsets.ModelViewSet):
    """
    API endpoint to view and edit postings
    this viewset provides default actions inherited from 'ModelViewset',
    theses are: 'list', 'create', 'destroy', 'retrieve', 'update'.
    the viewset also provides a custom action:
    'filter_postings': allows for querying postings by fields.
    """
    queryset = Posting.objects.all().order_by('status')
    serializer_class = PostingSerializer
    filterset_fields = ['id', 'title', 'description', 'user', 'created_at',
                        'expires_at', 'price', 'status']
    renderer_classes = [JSONRenderer]
    parser_classes = [JSONParser]

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

    @method_decorator(cache_page(60 * 60))
    @method_decorator(vary_on_headers("Authorization"))
    def list(self, request):
        return super().list(request)

    @method_decorator(cache_page(60 * 60))
    @method_decorator(vary_on_headers("Authorization"))
    def retrieve(self, request, pk=None):
        return super().retrieve(request, pk=None)

    def create(self, request):
        serializer = PostingSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse({"result":"posting added successfully."},
                            status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):

        posting = self.get_object()
        serializer = PostingSerializer(posting, data= request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse({"result":"posting updated"}, status=status.HTTP_200_OK)

class GigViewSet(JsonSchemaMixin, viewsets.ModelViewSet):
    """
    API endpoint to view and edit gigs
    this viewset provides default actions inherited from 'ModelViewset',
    theses are: 'list', 'create', 'destroy', 'retrieve', 'update'.
    the viewset also provides a custom action:
    'filter_gigs': allows for querying gigs by fields.
    """
    queryset = Gig.objects.all().order_by('status')
    serializer_class = GigSerializer
    filterset_fields = ['id', 'title', 'description', 'user',
                        'start_date', 'end_date', 'price', 'status']
    renderer_classes = [JSONRenderer]
    parser_classes = [JSONParser]

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

    @method_decorator(cache_page(60 * 60))
    @method_decorator(vary_on_headers("Authorization"))
    def list(self, request):
        return super().list(request)

    @method_decorator(cache_page(60 * 60))
    @method_decorator(vary_on_headers("Authorization"))
    def retrieve(self, request, pk=None):
        return super().retrieve(request, pk=None)

    def create(self, request):

        serializer = GigSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse({}, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        gig = self.get_object()
        serializer = GigSerializer(gig, data= request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse({}, status=status.HTTP_200_OK)
