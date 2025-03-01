"""
This module converts djando model instances into Python
data types. 
"""

from rest_framework import serializers
from gigwork.models import User, Gig, Posting

class UserSerializer(serializers.ModelSerializer):
    """
    convert 'User' model into a python dictionary
    """
    phone_number = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    role = serializers.CharField(required=False)
    class Meta:
        """
        this inner class specifies the model associated with the serializer
        """
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address', 'role']

class GigSerializer(serializers.ModelSerializer):
    """
    convert 'Gig' model into a python dictionary
    """
    class Meta:
        """
        this inner class specifies the model associated with the serializer
        """
        model = Gig
        fields = ['title', 'description', 'user', 'start_date', 'end_date', 'price', 'status']

class PostingSerializer(serializers.ModelSerializer):
    """
    convert 'Posting' model into a python dictionary
    """
    class Meta:
        """
        this inner class specifies the model associated with the serializer
        """
        model = Posting
        fields = ['title', 'description', 'user', 'created_at', 'expires_at', 'price', 'status']
