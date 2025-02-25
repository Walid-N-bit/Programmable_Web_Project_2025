from gigwork.models import User, Gig, Posting
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address', 'role']

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
