from gigwork.models import User, Gig, Posting
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    role = serializers.CharField(required=False)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 
                  'address', 'role']
        
class GigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gig
        fields = ['title', 'description', 'user', 'start_date', 
                  'end_date', 'price', 'status']

class PostingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posting
        fields = ['title', 'description', 'user', 'created_at', 
                  'expires_at', 'price', 'status']
