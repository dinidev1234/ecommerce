from django.urls import path
from .views import home, category_view, product_view, add_to_cart, \
    view_cart, remove_from_cart, increase_quantity, \
    decrease_quantity, checkout, order_confirmation, \
    sub_category_view, search_result

urlpatterns = [
    path('', home, name='home'),
    path('search/', search_result, name='search_results'),
    path('category/<int:category_pk>/', category_view, name='category'),
    path('category/<int:category_pk>/subcategory/<int:sub_category_pk>/',
         sub_category_view, name='sub_category'),
    path('category/<int:category_pk>/subcategory/<int:sub_category_pk>/product/<int:product_pk>/',
         product_view, name='product'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/',
         remove_from_cart, name='remove_from_cart'),
    path('increase_quantity/<int:product_id>/',
         increase_quantity, name='increase_quantity'),
    path('decrease_quantity/<int:product_id>/',
         decrease_quantity, name='decrease_quantity'),
    path('cart/', view_cart, name='view_cart'),
    path('checkout/', checkout, name='checkout'),
    path('order_confirmation/', order_confirmation, name='order_confirmation'),
]
