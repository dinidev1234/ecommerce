from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Product, Category


# Create your views here.


def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart = request.session.get('cart', [])
    id_list = list(map(lambda item: item['id'], cart)) #need to dont add added items in cart
    if product_id not in id_list:
        cart.append({
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'quantity': 1
        })
    request.session['cart'] = cart
    url = reverse('category', kwargs={'pk': product.category_id})
    return redirect(url)


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', [])
    cart = list(filter(lambda item: item.get('id') != product_id, cart))
    request.session['cart'] = cart
    return redirect('view_cart')


# Ваше представление или представление API для увеличения количества товара
def increase_quantity(request, product_id):
    cart = request.session.get('cart', [])
    for item in cart:
        if item.get('id') == product_id:
            # Увеличьте количество товара в этом словаре
            item['quantity'] = item.get('quantity', 0) + 1
            break

    request.session['cart'] = cart

    # Сохраните сессию
    request.session.modified = True
    return redirect('view_cart')


def decrease_quantity(request, product_id):
    cart = request.session.get('cart', [])
    for item in cart:
        if item.get('id') == product_id:
            if item['quantity'] >= 1:
                item['quantity'] = item.get('quantity', 0) - 1
            if item['quantity'] == 0:
                cart = list(filter(lambda item: item.get('id') != product_id, cart))

            break

    request.session['cart'] = cart

    # Сохраните сессию
    request.session.modified = True
    return redirect('view_cart')


def view_cart(request):
    cart = request.session.get('cart', [])
    price = sum([item.get('price') for item in cart])
    return render(request, 'cart.html', {'cart': cart, 'price': price })
#TODO make a plan for a checkout system


def category_view(request, pk):
    category = Category.objects.get(pk=pk)
    products = Product.objects.filter(category=category)
    cart = request.session.get('cart', [])

    return render(request, 'category.html', {'category': category,
                                             'products': products,
                                             })


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
