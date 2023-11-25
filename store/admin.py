from django.contrib import admin
from .models import Product, Category, Order, OrderItem, Subcategory

# Register your models here.

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Order)
admin.site.register(OrderItem)
