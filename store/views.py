from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Product, Category


# Create your views here.

def category_view(request, pk):
    category = Category.objects.get(pk=pk)
    products = Product.objects.filter(category=category)
    return render(request, 'category.html', {'category': category, 'products': products})


def product_view(request, category_pk, product_pk):
    product = Product.objects.get(pk=product_pk)
    return render(request, 'product.html', {'product': product})


def home(request):
    cats = Category.objects.all()
    return render(request, 'base.html', {'cats': cats})


def description(request):
    context = {}
    return render(request, 'description.html', context)


def delivery(request):
    context = {}
    return render(request, 'delivery.html', context)


def guarantee(request):
    context = {}
    return render(request, 'guarantee.html', context)


def contacts(request):
    context = {}
    return render(request, 'contacts.html', context)
