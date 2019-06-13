from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Shop, Product, Order, LineItem

# Create your views here.


def index(request):
    shops_list = Shop.objects.order_by('-added_date')
    context = {'shops_list': shops_list}
    return render(request, 'shops/index.html', context)


def shop(request, shop_id):
    s = get_object_or_404(Shop, pk=shop_id)
    context = {'shop': s}
    return render(request, 'shops/shop.html', context)


def products(request, shop_id):
    s = get_object_or_404(Shop, pk=shop_id)
    products_list = s.get_products().order_by('-added_date')
    context = {'shop_id': shop_id, 'products_list': products_list}
    return render(request, 'shops/products.html', context)


def product(request, shop_id, product_id):
    prod = get_object_or_404(Product, pk=product_id)
    context = {'shop_id': shop_id, 'product': prod}
    return render(request, 'shops/product.html', context)


def orders(request, shop_id):
    s = get_object_or_404(Shop, pk=shop_id)
    orders_list = s.get_orders().order_by('-added_date')
    context = {'shop_id': shop_id, 'orders_list': orders_list}
    return render(request, 'shops/orders.html', context)


def order(request, shop_id, order_id):
    ord = get_object_or_404(Order, pk=order_id)
    context = {'shop_id': shop_id, 'order': ord, 'items': ord.lineitems.all()}
    return render(request, 'shops/order.html', context)


def lineitem(request, shop_id, lineitem_id):
    item = get_object_or_404(LineItem, pk=lineitem_id)
    context = {'shop_id': shop_id, 'lineitem': item}
    return render(request, 'shops/lineitem.html', context)