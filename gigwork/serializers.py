"""
This module converts djando model instances into Python
data types.

Source for the general structure of the module:
https://www.django-rest-framework.org/tutorial/quickstart/#serializers
https://www.django-rest-framework.org/api-guide/serializers/#overriding-serialization-and-deserialization-behavior
https://www.django-rest-framework.org/api-guide/relations/#nested-relationships
https://www.django-rest-framework.org/api-guide/relations/#primarykeyrelatedfield
"""
from decimal import Decimal
from rest_framework import serializers, status
from django.http import JsonResponse
from gigwork.models import User, Gig, Posting
from rest_framework.reverse import reverse

class UserSerializer(serializers.ModelSerializer):
    """
    convert 'User' model into a python dictionary
    """
    phone_number = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    class Meta:
        """
        this inner class specifies the model associated with the serializer
        """
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'address']

class PublicUserSerializer(serializers.ModelSerializer):
    """
    convert 'User' model into a python dictionary.
    this class contains only fields that would be available to other users than the owner.
    """
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['@controls'] = {
        "self": { "href": reverse("users-detail", args=[data['id']])}
                 }
        return data
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']

class PostingSerializer(serializers.ModelSerializer):
    """
    convert 'Posting' model into a python dictionary
    """
    # user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    owner = PublicUserSerializer(read_only=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)

    def to_internal_value(self, data):
        price = data.get('price')
        if price <= 0:
            raise serializers.ValidationError({"error":"price must be a positive non-zero value"})
        return data

    class Meta:
        """
        this inner class specifies the model associated with the serializer
        """
        model = Posting
        fields = ['id', 'title', 'owner', 'description', 'created_at', 'expires_at', 'price', 'status']

class GigSerializer(serializers.ModelSerializer):
    """
    convert 'Gig' model into a python dictionary
    """
    owner = PublicUserSerializer(read_only=True)
    posting = serializers.PrimaryKeyRelatedField(queryset=Posting.objects.all(), many=False)
    class Meta:
        """
        this inner class specifies the model associated with the serializer
        """
        model = Gig
        fields = ['id', 'owner', 'posting', 'start_date', 'end_date', 'status']
