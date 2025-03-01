from django.shortcuts import render

from gigwork.models import User, Gig, Posting
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.http import HttpResponse, JsonResponse
from rest_framework.authtoken.models import Token

from gigwork.serializers import UserSerializer, GigSerializer, PostingSerializer

class UserViewSet(viewsets.ModelViewSet):           #API endpoint to view and edit users
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer

    # 
    def get_permissions(self):
        if self.action == 'new_user':
            permission_classes = []
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    authentication_classes = [TokenAuthentication]

    @action(detail=False, methods=['post']) 
    def new_user(self, request):    
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        return JsonResponse({"Token": token.key}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def filter_users(self, request):
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address', 'role']
        user_list = User.objects.all() 
        for field in fields:
            f = request.query_params.get(field)
            if f != None:
                kwags = {field: f}
                user_list = user_list.filter(**kwags)
        serialized = UserSerializer(user_list, many=True)
        return JsonResponse(serialized.data, safe=False)
    
class GigViewSet(viewsets.ModelViewSet):                #API endpoint to view and edit gigs
    queryset = Gig.objects.all().order_by('status')
    serializer_class = GigSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    @action(detail=False, methods=['get'])
    def filter_gigs(self, request):
        fields = ['title', 'description', 'user', 'start_date', 
                  'end_date', 'price', 'status']
        gig_list = Gig.objects.all() 
        for field in fields:
            f = request.query_params.get(field)
            if f != None:
                kwags = {field: f}
                gig_list = gig_list.filter(**kwags)
        serialized = UserSerializer(gig_list, many=True)
        return JsonResponse(serialized.data, safe=False)

class PostingViewSet(viewsets.ModelViewSet):            #API endpoint to view and edit postings
    queryset = Posting.objects.all().order_by('status')
    serializer_class = PostingSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    @action(detail=False, methods=['get'])
    def filter_postings(self, request):
        fields = ['title', 'description', 'user', 'created_at', 
                  'expires_at', 'price', 'status']
        posting_list = Gig.objects.all() 
        for field in fields:
            f = request.query_params.get(field)
            if f != None:
                kwags = {field: f}
                posting_list = posting_list.filter(**kwags)
        serialized = UserSerializer(posting_list, many=True)
        return JsonResponse(serialized.data, safe=False)
