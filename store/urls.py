from django.urls import path
from .views import ProductListView, CategoryListView, description, delivery, guarantee, contacts

urlpatterns = [
    path('', CategoryListView.as_view(), name='home'),
    path('about-company/', description, name='description'),
    path('delivery/', delivery, name='delivery'),
    path('guarantee/', guarantee, name='guarantee'),
    path('contacts/', contacts, name='contacts'),
]