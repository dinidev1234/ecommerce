from django.shortcuts import render
from django.views.generic import ListView

from .models import Product, Category


# Create your views here.
class ProductListView(ListView):
    model = Product
    context_object_name = 'products'


class CategoryListView(ListView):
    model = Category
    context_object_name = 'cats'
    template_name = 'base.html'


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
