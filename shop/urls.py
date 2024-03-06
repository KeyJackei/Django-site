from django.contrib import admin
from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='main'),
    path('product/<int:id>/', ProductView.as_view(), name='product-detail'),
    path('catalog/', ProductListView.as_view(), name='catalog'),
    # path('premium/', PremiumListView.as_view(), name='premium'),
    path('basket/', BasketListView.as_view(), name='basket'),
    path('basket-add/<int:product_id>/', add_to_basket, name='basket_add'),
    path('basket-delete/<int:id>/', remove_all_from_basket, name='basket_delete'),
    path('search', SearchListView.as_view(), name='search'),
    path('create-order', create_order, name='create_order'),
    path('basket-del/<int:product_id>/', remove_one_from_basket, name='basket_del')
]