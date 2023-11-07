from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path
from .views import home, description, delivery, guarantee, contacts, category_view, product_view, register, add_to_cart, \
    view_cart

urlpatterns = [
    path('', home, name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
    path('about-company/', description, name='description'),
    path('delivery/', delivery, name='delivery'),
    path('guarantee/', guarantee, name='guarantee'),
    path('contacts/', contacts, name='contacts'),
    path('category/<int:pk>/', category_view, name='category'),
    path('category/<int:category_pk>/product/<int:product_pk>/', product_view, name='product'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),

]