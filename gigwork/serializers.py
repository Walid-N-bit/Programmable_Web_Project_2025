"""
This module converts djando model instances into Python
data types. 

Source for the general structure of the module:
https://www.django-rest-framework.org/tutorial/quickstart/#serializers
https://www.django-rest-framework.org/api-guide/serializers/#overriding-serialization-and-deserialization-behavior
"""
from decimal import Decimal
from rest_framework import serializers, status
from django.http import JsonResponse
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
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'address', 'role']

class PostingSerializer(serializers.ModelSerializer):
    """
    convert 'Posting' model into a python dictionary
    """
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)

    def to_internal_value(self, data):
        price = data.get('price')
        if not isinstance(price, (int, float, Decimal)):
            raise serializers.ValidationError({"error":"price must be a number"})
        if price <= 0:
            raise serializers.ValidationError({"error":"price must be a positive non-zero value"})
        return data
    
    class Meta:
        """
        this inner class specifies the model associated with the serializer
        """
        model = Posting
        fields = ['id', 'title', 'description', 'user', 'created_at', 'expires_at', 'price', 'status']
    
        
class GigSerializer(serializers.ModelSerializer):
    """
    convert 'Gig' model into a python dictionary
    """
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        """
        this inner class specifies the model associated with the serializer
        """
        model = Gig
        fields = ['id', 'title', 'description', 'user', 'start_date', 'end_date', 'price', 'status']
