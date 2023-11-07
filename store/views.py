from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView

from .models import Product, Category


# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to a success page
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart = request.session.get('cart', [])
    cart.append({
        'id': product.id,
        'name': product.name,
        'price': float(product.price),
    })
    request.session['cart'] = cart
    return redirect('home')


def view_cart(request):
    cart = request.session.get('cart', [])
    return render(request, 'cart.html', {'cart': cart})


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
