from django.contrib.auth.models import User
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
    is_published = models.BooleanField(default=True, verbose_name='Published')

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

