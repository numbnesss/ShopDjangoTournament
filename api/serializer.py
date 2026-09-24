from rest_framework import serializers
from . import models


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 3}}

        def create(self, data):
            return models.User.objects.create_user(**data)


class AuthSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['id', 'name', 'description']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ['id', 'name', 'description', 'price', 'image_url']


class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = models.Order
        fields = ['id', 'status', 'product']
