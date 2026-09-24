from django.urls import path
from .views import *

app_name = "ad"

urlpatterns = [
    path('', Auth.as_view(), name="auth"),
    path('logout', Logout.as_view(), name="logout"),
    path('categories', Categories.as_view(), name="categories"),
    path('categories/create', CategoryCreate.as_view(), name="category_create"),
    path('categories/<int:cat_id>', CategoryDetails.as_view(), name="category_details"),
    path('categories/<int:cat_id>/edit', CategoryEdit.as_view(), name="category_edit"),
    path('categories/<int:cat_id>/delete', CategoryDelete.as_view(), name="category_delete"),
    path('categories/<int:cat_id>/products/create', ProductCreate.as_view(), name="product_create"),
    path('categories/<int:cat_id>/products/<int:prod_id>', ProductDetails.as_view(), name="product_details"),
    path('categories/<int:cat_id>/products/<int:prod_id>/edit', ProductEdit.as_view(), name="product_edit"),
    path('categories/<int:cat_id>/products/<int:prod_id>/delete', ProductDelete.as_view(), name="product_delete"),
    path('orders', Orders.as_view(), name="orders"),
]
