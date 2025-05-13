"""
This module contains viewsets for the API. Viewsets in Django are called "resources"
in other frameworks. They provide actions to execute GEt, POST, PUT, DELETE, PATCH requests.

Sources:
https://www.django-rest-framework.org/tutorial/quickstart/#views
https://www.django-rest-framework.org/api-guide/exceptions/#apiexception
https://lovelace.oulu.fi/ohjelmoitava-web/ohjelmoitava-web/implementing-rest-apis-with-flask/#dynamic-schemas-static-methods
https://www.django-rest-framework.org/api-guide/caching/
https://docs.djangoproject.com/en/5.2/ref/urlresolvers/#reverse
https://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/#associating-snippets-with-users
https://www.django-rest-framework.org/api-guide/views/
https://www.django-rest-framework.org/api-guide/permissions/#api-reference
"""

# standard library
from jsonschema import validate, ValidationError

# Django
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.vary import vary_on_headers
from django.views.decorators.cache import cache_page

# Django rest framework
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions, viewsets, status
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import UnsupportedMediaType, ParseError
from rest_framework.reverse import reverse

# local modules
from gigwork.masonbuilder import MasonBuilder
from gigwork.serializers import UserSerializer, GigSerializer, PostingSerializer
from gigwork.models import User, Gig, Posting
from gigwork.custom_permissions import IsOwnerOrReadOnly, IsSelfOrReadOnly

class JsonSchemaMixin:
    def json_schema_validation(self, request, *args, **kwargs):
        if request.content_type != 'application/json':
            raise UnsupportedMediaType(request.content_type)
        try:
            validate(request.data, self.json_schema())
        except ValidationError as e:
            raise ParseError(detail=str(e)) from e


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def api_root(request):
    return JsonResponse(
        {
            "@controls": {
                "self": {"href": reverse("api-root", request=request)},
                "users": {"href": reverse("users-list", request=request)},
                "postings": {"href": reverse("postings-list", request=request)},
                "gigs": {"href": reverse("gigs-list", request=request)},
            }
        }
    )


class UserViewSet(JsonSchemaMixin, viewsets.ModelViewSet):
    """
    API endpoint to view and edit users
    this viewset provides default actions inherited from 'ModelViewSet',
    theses are: 'list', 'create', 'destroy', 'retrieve', 'update'.
    """

    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer
    filterset_fields = [
        "id",
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "address",
    ]
    renderer_classes = [JSONRenderer]
    parser_classes = [JSONParser]

    @staticmethod
    def json_schema():
        schema = {
            "type": "object",
            "required": ["first_name", "last_name", "email"],
            "properties": {
                "first_name": {"type": "string"},
                "last_name": {"type": "string"},
                "email": {"type": "string"},
                "phone_number": {"type": "string"},
                "address": {"type": "string"},
            },
        }
        return schema

    def get_permissions(self):
        """
        The purpose of this method is to allow for creating new users without
        being blocked by the authentication and permission schemes.
        """
        if self.action == "create":
            permission_classes = []
        else:
            permission_classes = [permissions.IsAuthenticated, IsSelfOrReadOnly]
        return [permission() for permission in permission_classes]

    authentication_classes = [TokenAuthentication]

    # permission_classes = []
    # authentication_classes = []

    def get_object(self):
        obj = User.objects.get(pk = self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj

    @method_decorator(cache_page(60 * 5))
    @method_decorator(vary_on_headers("Authorization"))
    def list(self, request):
        response = super().list(request)
        body = MasonBuilder(items=[])
        for user in response.data:
            item = MasonBuilder(user)
            self_url = reverse("users-detail", kwargs={"pk": user["id"]})
            item.add_control("self", self_url)
            body["items"].append(item)

        base_url = request.build_absolute_uri(reverse("users-list"))
        body.add_control("self", base_url)
        body.add_control(
            ctrl_name="filter users by field",
            href=base_url + "{?id,first_name,last_name,email,phone_number,address}",
        )

        body.add_control_post(
            ctrl_name="user: create",
            title="add a new user",
            href=request.build_absolute_uri(),
            schema=UserViewSet.json_schema(),
        )

        return JsonResponse(body)

    @method_decorator(cache_page(60 * 5))
    @method_decorator(vary_on_headers("Authorization"))
    def retrieve(self, request, pk=None):
        response = super().retrieve(request, pk=None)
        body = MasonBuilder(response.data)
        self_url = reverse("users-detail", kwargs={"pk": response.data["id"]})

        body.add_control("self", self_url)

        body.add_control_put(
            title="update existing user",
            href=self_url,
            schema=UserViewSet.json_schema(),
        )
        body.add_control_delete(title="remove a user", href=self_url)
        return JsonResponse(body)

    def create(self, request, *args, **kwargs):
        """
        create new user, return authentication token for that user.
        data is sent from the client in json format, required fields are: first_name,
        last_name, email.
        """
        self.json_schema_validation(request, *args, **kwargs)
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
    """

    queryset = Posting.objects.all().order_by("status")
    serializer_class = PostingSerializer
    filterset_fields = [
        "id",
        "title",
        "description",
        "owner",
        "created_at",
        "expires_at",
        "price",
        "status",
    ]
    renderer_classes = [JSONRenderer]
    parser_classes = [JSONParser]

    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    # authentication_classes = []
    # permission_classes = []

    @staticmethod
    def json_schema():
        schema = {
            "type": "object",
            "required": ["title", "description", "price"],
            "properties": {
                "title": {"type": "string"},
                "description": {"type": "string"},
                "created_at": {"type": "string"},
                "expires_at": {"type": "string"},
                "price": {"type": "number"},
                "status": {"type": "string"},
            },
        }
        return schema

    def get_object(self):
        obj = Posting.objects.get(pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    @method_decorator(cache_page(60 * 5))
    @method_decorator(vary_on_headers("Authorization"))
    def list(self, request, *args, **kwargs):
        response = super().list(request)
        body = MasonBuilder(items=[])
        for posting in response.data:
            item = MasonBuilder(posting)
            self_url = reverse("postings-detail", kwargs={"pk": posting["id"]})
            item.add_control("self", self_url)
            body["items"].append(item)

        base_url = request.build_absolute_uri(reverse("postings-list"))
        body.add_control("self", base_url)
        body.add_control(
            ctrl_name="filter postings by field",
            href=base_url + "{?id, title, description, owner, created_at,"
            "expires_at, price, status}",
        )

        body.add_control_post(
            ctrl_name="posting: create",
            title="add a new posting",
            href=base_url,
            schema=PostingViewSet.json_schema(),
        )

        return JsonResponse(body)

    @method_decorator(cache_page(60 * 5))
    @method_decorator(vary_on_headers("Authorization"))
    def retrieve(self, request, pk=None, *args, **kwargs):
        response = super().retrieve(request, pk=None)
        body = MasonBuilder(response.data)
        self_url = reverse("postings-detail", kwargs={"pk": response.data["id"]})
        body.add_control("self", self_url)
        body.add_control_put(
            title="update existing posting",
            href=self_url,
            schema=PostingViewSet.json_schema(),
        )
        body.add_control_delete(title="remove a posting", href=self_url)
        return JsonResponse(body)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        self.json_schema_validation(request, *args, **kwargs)
        serializer = PostingSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return JsonResponse(
            {"result": "posting added successfully."}, status=status.HTTP_201_CREATED
        )

    def update(self, request, pk=None, *args, **kwargs):
        self.json_schema_validation(request, *args, **kwargs)
        posting = self.get_object()
        serializer = PostingSerializer(posting, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse({"result": "posting updated"}, status=status.HTTP_200_OK)


class GigViewSet(JsonSchemaMixin, viewsets.ModelViewSet):
    """
    API endpoint to view and edit gigs
    this viewset provides default actions inherited from 'ModelViewset',
    theses are: 'list', 'create', 'destroy', 'retrieve', 'update'.
    """

    queryset = Gig.objects.all().order_by("status")
    serializer_class = GigSerializer
    filterset_fields = ["id", "owner", "start_date", "end_date", "status"]
    renderer_classes = [JSONRenderer]
    parser_classes = [JSONParser]

    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    # authentication_classes = []
    # permission_classes = []

    @staticmethod
    def json_schema():
        schema = {
            "type": "object",
            "required": ["posting"],
            "properties": {
                "posting": {"type": "number"},
                "start_date": {"type": "string"},
                "end_date": {"type": "string"},
                "status": {"type": "string"},
            },
        }
        return schema
    
    def get_object(self):
        obj = Gig.objects.get(pk = self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj
    
    @method_decorator(cache_page(60 * 5))
    @method_decorator(vary_on_headers("Authorization"))
    def list(self, request, *args, **kwargs):
        response = super().list(request)
        body = MasonBuilder(items=[])
        for gig in response.data:
            item = MasonBuilder(gig)
            self_url = reverse("gigs-detail", kwargs={"pk": gig["id"]})
            item.add_control("self", self_url)
            body["items"].append(item)

        base_url = request.build_absolute_uri(reverse("gigs-list"))
        body.add_control("self", base_url)
        body.add_control(
            ctrl_name="filter gigs by field",
            href=base_url + "{?id, owner, posting, start_date, end_date, status}",
        )

        body.add_control_post(
            ctrl_name="gig: create",
            title="add a new gig",
            href=base_url,
            schema=GigViewSet.json_schema(),
        )
        return JsonResponse(body)

    @method_decorator(cache_page(60 * 5))
    @method_decorator(vary_on_headers("Authorization"))
    def retrieve(self, request, pk=None, *args, **kwargs):
        response = super().retrieve(request, pk=None)
        body = MasonBuilder(response.data)
        self_url = reverse("gigs-detail", kwargs={"pk": response.data["id"]})
        body.add_control("self", self_url)
        body.add_control_put(
            title="update existing gig", href=self_url, schema=GigViewSet.json_schema()
        )
        body.add_control_delete(title="remove a gig", href=self_url)
        return JsonResponse(body)

    def perform_create(self, serializer):
        gig = serializer.save(owner=self.request.user)
        gig.posting.status = "accepted"
        gig.posting.save()

    def create(self, request, *args, **kwargs):
        self.json_schema_validation(request, *args, **kwargs)
        serializer = GigSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return JsonResponse({"result": "gig added"}, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, *args, **kwargs):
        self.json_schema_validation(request, *args, **kwargs)
        gig = self.get_object()
        serializer = GigSerializer(gig, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse({"result": "gig updated"}, status=status.HTTP_200_OK)
