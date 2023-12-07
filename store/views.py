from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import OrderForm
from .models import Product, Category, Order, OrderItem, Subcategory
import logging

logger = logging.getLogger('main')


# Create your views here.
def search_result(request):
    query = request.GET.get('query', None)  # Получаем значение параметра 'query' из запроса
    results = Product.objects.filter(
        name__icontains=query) | Product.objects.filter(description__icontains=query
                                                        )
    return render(request, 'search_results.html', {'query': query,
                                                   'results': results})


def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart = request.session.get('cart', [])
    id_list = list(map(lambda item: item['id'], cart))   # need to don't add added items in cart
    if product_id not in id_list:
        cart.append({
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'quantity': 1
        })
        request.session['cart'] = cart
    logger.info(f'product with ID:{product_id} added to cart')
    return redirect('view_cart')


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', [])
    cart = list(filter(lambda item: item.get('id') != product_id, cart))
    request.session['cart'] = cart
    logger.info(f'product with ID:{product_id} removed from cart')
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
    logger.info('quantity increased')
    return redirect('view_cart')


def decrease_quantity(request, product_id):
    cart = request.session.get('cart', [])
    for item in cart:
        if item.get('id') == product_id:
            if item['quantity'] >= 1:
                item['quantity'] = item.get('quantity', 0) - 1
            if item['quantity'] == 0:
                cart = list(
                    filter(
                        lambda item: item.get('id') != product_id, cart
                    )
                )

            break

    request.session['cart'] = cart

    # Сохраните сессию
    request.session.modified = True
    logger.info(f'quantity decreased')
    return redirect('view_cart')


def view_cart(request):
    logger.info('view_cart')
    cart = request.session.get('cart', [])
    price = sum([item.get('price') * item.get('quantity') for item in cart])
    return render(request, 'cart.html', {'cart': cart, 'price': price})


def checkout(request):
    cart = request.session.get('cart', [])
    if not cart:
        return HttpResponse('Cart is empty')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            phone = form.cleaned_data['phone']
            comment = form.cleaned_data['comment']
            total_price = sum(
                [item.get('price') * item.get('quantity') for item in cart]
            )

            order = Order(
                name=name,
                address=address,
                phone=phone,
                comment=comment,
                total_price=total_price,
                session_key=request.session.session_key
            )
            order.save()
            for item in cart:
                product = Product.objects.get(pk=item['id'])
                order_item = OrderItem(
                    order=order,
                    product=product,
                    price=item['price'],
                    quantity=item['quantity']

                )
                order_item.save()
            return redirect('order_confirmation')
    else:
        form = OrderForm()

    return render(request, 'checkout.html', {'form': form})


def order_confirmation(request):
    session_key = request.session.session_key
    order = Order.objects.filter(
        session_key=session_key).last()
    if order:
        logger.info(f'order with ID{order.pk} confirmed')
        request.session['cart'] = []
        return render(request, 'order_confirmation.html', {'order': order})
    else:
        return HttpResponse('Order not found')


def category_view(request, category_pk):
    logger.info(f'displayed sub_cats from category ID{category_pk}')
    category = Category.objects.get(pk=category_pk)
    sub_cats = Subcategory.objects.filter(category_id=category_pk)

    return render(request, 'category.html', {'category': category,
                                             'sub_cats': sub_cats})


def sub_category_view(request, category_pk, sub_category_pk):
    logger.info(f'displayed products from sub_category ID{sub_category_pk}')
    products = Product.objects.filter(sub_category_id=sub_category_pk)
    return render(request, 'sub_category.html', {'products': products,
                                                 'category_pk': category_pk,
                                                 'sub_category_pk': sub_category_pk})


def product_view(request, category_pk, sub_category_pk, product_pk):
    logger.info(f'displayed product with ID:{product_pk}')
    product = Product.objects.get(pk=product_pk)
    return render(request, 'product.html', {'product': product})


def home(request):
    return render(request, 'base.html', {})
