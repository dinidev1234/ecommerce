from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import OrderForm
from .models import Product, Category, Order


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
    price = sum([item.get('price') * item.get('quantity') for item in cart])
    return render(request, 'cart.html', {'cart': cart, 'price': price })
#TODO make a plan for a checkout system


def checkout(request):
    cart = request.session.get('cart', [])
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Получение данных из формы
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            phone = form.cleaned_data['phone']
            products = [item['id'] for item in cart]
            comment = form.cleaned_data['comment']
            total_price = sum([item.get('price') * item.get('quantity') for item in cart])

            # Создание заказа и установка значения для поля price
            order = Order(
                name=name,
                address=address,
                phone=phone,
                comment=comment,
                total_price=total_price,
                session_key=request.session.session_key
            )
            order.save()
            order.products.add(*products)
            return redirect('order_confirmation')
    else:
        form = OrderForm()

    return render(request, 'checkout.html', {'form': form})


def order_confirmation(request):
    session_key = request.session.session_key
    order = Order.objects.filter(session_key=session_key).last()
    if order:
        request.session['cart'] = []
        return render(request, 'order_confirmation.html', {'order': order})
    else:
        return HttpResponse('Order not found')


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
