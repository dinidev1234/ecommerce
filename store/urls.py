from django.urls import path
from .views import home, description, delivery, guarantee, contacts, category_view, product_view

urlpatterns = [
    path('', home, name='home'),
    path('about-company/', description, name='description'),
    path('delivery/', delivery, name='delivery'),
    path('guarantee/', guarantee, name='guarantee'),
    path('contacts/', contacts, name='contacts'),
    path('category/<int:pk>/', category_view, name='category'),
    path('category/<int:category_pk>/product/<int:product_pk>/', product_view, name='product')

]