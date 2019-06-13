from django.urls import path

from . import views

app_name = 'shops'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:shop_id>', views.shop, name='shop'),
    path('<int:shop_id>/products', views.products, name='products'),
    path('<int:shop_id>/products/<int:product_id>', views.product, name='product'),
    path('<int:shop_id>/orders', views.orders, name='orders'),
    path('<int:shop_id>/orders/<int:order_id>', views.order, name='order'),
]