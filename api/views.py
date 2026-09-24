import requests
from django.conf import settings
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from . import models, serializer
from .utils import error


class Registration(APIView):
    def post(self, req):
        s = serializer.RegistrationSerializer(data=req.data)
        s.is_valid(raise_exception=True)
        s.save()
        return Response({'success': True}, status=201)


class Auth(APIView):
    def post(self, req):
        s = serializer.AuthSerializer(data=req.data)
        s.is_valid(raise_exception=True)
        user = authenticate(**s.validated_data)
        if user is None:
            return error('Invalid data', {'email': ['Invalid data']})
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


class Categories(APIView):
    def get(self, req):
        s = serializer.CategorySerializer(models.Category.objects.all(), many=True)
        return Response({'data': s.data})


class CategoryProducts(APIView):
    def get(self, req, cat_id):
        category = get_object_or_404(models.Category, pk=cat_id)
        s = serializer.ProductSerializer(category.product_set.all(), many=True, context={'request': req})
        return Response({'data': s.data})


class Product(APIView):
    def get(self, req, prod_id):
        product = get_object_or_404(models.Product, pk=prod_id)
        s = serializer.ProductSerializer(product, context={'request': req})
        return Response({'data': s.data})


class ProductBuy(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, req, prod_id):
        product = get_object_or_404(models.Product, pk=prod_id)
        data = requests.post(settings.PAYMENT_GATEWAY_URL, json={
            'price': float(product.price),
            'webhook_url': req.build_absolute_url('/api/payment-webhook'),
        }).json()
        models.Order.objects.create(user=req.user, product=product, payment_order_id=data['order_id'])
        return Response({'pay_url': data['pay_url']})


class PaymentWebhook(APIView):
    def post(self, req):
        status = req.data.get('status')
        if status in ('success', 'failed'):
            models.Order.objects.filter(payment_order_id=req.data.get('order_id')).update(status=status)
        return Response(status=204)


class Orders(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, req):
        orders = models.Order.objects.filter(user=req.user)
        s = serializer.OrderSerializer(orders, many=True, context={'request': req})
        return Response({'data': s.data})
