from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView

from .models import *

def index(request):

    return render(request, 'shop/main.html')


class ProductListView(ListView):
    '''
    Вывод товаров для мужчин и женщин
    '''
    template_name = 'shop/catalog.html'

    def get_queryset(self):
        queryset = Product.objects.all()

        season = self.request.GET.get('season')
        brands = self.request.GET.getlist('brand')
        categories = self.request.GET.getlist('category')

        if season:
            queryset = queryset.filter(season=season)

        if brands:
            brand_filters = Q()
            for brand in brands:
                brand_filters |= Q(manufacturer=brand)
            queryset = queryset.filter(brand_filters)

        if categories:
            category_filters = Q()
            for category in categories:
                category_filters |= Q(category=category)
            queryset = queryset.filter(category_filters)

        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        brands = Manufacturer.objects.values()
        categories = Category.objects.values()

        page_number = request.GET.get('page')
        paginator = Paginator(queryset, 6)
        page = paginator.get_page(page_number)

        print(brands)
        return render(request,
                      self.template_name,
                      {'products': page,
                       'brands': brands,
                       'categories': categories
                       }
                      )


class ProductView(View):
    model = Product
    template_name = 'shop/product.html'
    queryset = Product.objects.all()

    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(self.queryset, id=id)

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        context = {'product': instance}

        return render(request, self.template_name, context)


class SearchListView(ListView):
    """
    Поиск
    """

    template_name = 'shop/search.html'


    def get_queryset(self):
        return Product.objects.filter(name__icontains=self.request.GET.get('query'))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        category = Category.objects.all()
        context['categories'] = category

        context['query'] = self.request.GET.get('query')
        return context


class BasketListView(ListView):
    template_name = 'shop/cart.html'

    def get_queryset(self):
        return Basket.objects.filter(user=self.request.user)

    def get_total_quantity(self):
        baskets = self.get_queryset()

        return sum(basket.quantity for basket in baskets)

    def get_total_sum(self):
        baskets = self.get_queryset()
        return sum(basket.sum() for basket in baskets)

    def get(self, request):
        context = {
            'object_list': self.get_queryset(),
            'total_quantity': self.get_total_quantity(),
            'total_sum': self.get_total_sum()
        }
        return render(request, self.template_name, context)


def add_to_basket(request, product_id):
    current_page = request.META.get('HTTP_REFERER')
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)

        return HttpResponseRedirect(current_page)

    basket = baskets.first()
    basket.quantity += 1
    basket.save()

    return HttpResponseRedirect(current_page)


def remove_all_from_basket(request, id):
    basket = Basket.objects.get(id=id)
    basket.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_one_from_basket(request, product_id):
    current_page = request.META.get('HTTP_REFERER')
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if baskets.exists():
        basket = baskets.first()
        if basket.quantity == 1:
            baskets.delete()

            return HttpResponseRedirect(current_page)

        basket = baskets.first()
        basket.quantity -= 1
        basket.save()

        return HttpResponseRedirect(current_page)


def create_order(request):
    """
    Создать заказ
    """
    user = request.user

    basket_items = Basket.objects.filter(user=user)

    if basket_items.exists():
        order = Order.objects.create(user=user)

        for basket_item in basket_items:
            order_item = OrderItem.objects.create(
                product=basket_item.product,
                quantity=basket_item.quantity,
                price=basket_item.product.price * basket_item.quantity
            )
            order.items.add(order_item)

        basket_items.delete()

        return redirect('main')


