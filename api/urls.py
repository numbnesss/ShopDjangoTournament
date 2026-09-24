from django.urls import path
from .views import *

urlpatterns = [
    path('registration', Registration.as_view()),
    path('auth', Auth.as_view()),
    path('categories', Categories.as_view()),
    path('categories/<int:cat_id>/products', CategoryProducts.as_view()),
    path('products/<int:prod_id>', Product.as_view()),
    path('products/<int:prod_id>/buy', ProductBuy.as_view()),
    path('payment-webhook', PaymentWebhook.as_view()),
    path('orders', Orders.as_view()),
]
