from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.db import models


class Category(models.Model):
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name='products')
    image = models.ImageField(upload_to='product_images/%Y/%m/%d')
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    is_published = models.BooleanField(default=True, verbose_name='is_available')

    def __str__(self):
        return self.name


class Order(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    products = models.ManyToManyField(Product, blank=True)  # Позволяет полю быть пустым в формах
    comment = models.CharField(max_length=255, blank=False, null=True)  # Позволяет быть пустым и в базе данных
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Значение по умолчанию
    date_ordered = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(max_length=32, blank=True, null=True)


    def __str__(self):
        return f'Order ID: {self.id}, User: {self.name}, Total Price: {self.total_price}'
