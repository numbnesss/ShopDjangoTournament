from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.core.validators import MinValueValidator
from django.conf import settings


class UserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        return self.create_user(email, password, is_staff=True, is_superuser=True, **kwargs)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class Category(models.Model):
    name = models.CharField(max_length=15)
    description = models.CharField(max_length=50, blank=True, default='')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=50, blank=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(10.01)])
    image_url = models.ImageField(upload_to='products/')
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)


class Order(models.Model):
    STATUSES = [('pending', 'pending'), ('success', 'success'), ('failed', 'failed')]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUSES, default='pending')
    payment_order_id = models.CharField(max_length=100)
