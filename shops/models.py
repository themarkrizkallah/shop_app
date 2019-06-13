import sys
import time
import random

from django.db import models
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.


# Generates a random 16 character order number
def order_number():
    order_num = str(int(round(time.time() * 1000)))
    order_num += str(random.randrange(10))
    order_num = [order_num[:4], order_num[4:10], order_num[10:]]
    order_num = '-'.join(order_num)

    return order_num


# Shop class
class Shop(models.Model):
    shop_name = models.CharField(max_length=30, unique=True)
    added_date = models.DateTimeField('date added')

    # Creates and returns a shop with shop_name
    @staticmethod
    def create(shop_name):
        if 0 < len(shop_name) < 31:
            shop = Shop(shop_name=shop_name, added_date=timezone.now())
            shop.save()
        else:
            print("Shop name is invalid.\nPlease try again.", file=sys.stderr)

        return Shop.objects.get(shop_name=shop_name)

    # Returns a shop with shop_name
    @staticmethod
    def get(shop_name):
        try:
            return Shop.objects.get(shop_name=shop_name)
        except ObjectDoesNotExist:
            print("Not a real shop, please try again.", file=sys.stderr)

    # Returns a queryset of all the available shops
    @staticmethod
    def get_shops():
        return Shop.objects.all()

    def __str__(self):
        return self.shop_name

    # Change the shop_name to new_name
    def change_name(self, new_name):
        if 0 < len(new_name) < 31:
            self.shop_name = new_name
            self.save()
        else:
            print("Did not change the shop name, new_name is invalid.", file=sys.stderr)

    # Returns a queryset of products in a shop
    def get_products(self):
        return self.product_set.all()

    # Returns a queryset of orders in a shop
    def get_orders(self):
        return self.order_set.all()

    # Returns a Product with product_name
    def get_product(self, product_name):
        try:
            return self.product_set.get(product_name=product_name)
        except ObjectDoesNotExist:
            print("Product not found, please try again.", file=sys.stderr)

    # Returns an Order with order_num
    def get_order(self, order_num):
        try:
            return self.order_set.get(order_num=order_num)
        except:
            print("Order not found, please try again.", file=sys.stderr)

    # Creates and adds a product to shop with product_name and returns the product
    def create_product(self, product_name):
        try:
            if 0 < len(product_name) < 31:
                product = self.product_set.create(product_name=product_name, added_date=timezone.now())
                return product
            else:
                print("Product name is invalid.\nPlease try again.", file=sys.stderr)
        except ValueError:
            print("Did not create product, %s not a shop.\nPlease try again.", self.shop_name, file=sys.stderr)

    # Creates and adds an order to shop and returns the order
    def create_order(self):
        try:
            order_num = order_number()
            order = self.order_set.create(order_num=order_num, added_date=timezone.now())
            return order
        except ValueError:
            print("Did not create order, %s not a shop.\nPlease try again.", self.shop_name, file=sys.stderr)

    # Adds an existing product to shop
    def add_product(self, product):
        try:
            self.product_set.add(product)
        except ValueError:
            print("Did not add product, %s not a shop.\nPlease try again.", self.shop_name, file=sys.stderr)

    # Adds an existing order to shop
    def add_order(self, order):
        try:
            self.order_set.add(order)
        except ValueError:
            print("Did not add order, %s not a shop.\nPlease try again.", self.shop_name, file=sys.stderr)


# Product class
class Product(models.Model):
    product_name = models.CharField(max_length=30, unique=True)
    value = models.DecimalField(default=0, max_digits=9, decimal_places=2)
    added_date = models.DateTimeField('date added')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name + ': $' + str(self.value)

    # Return product_name
    def get_name(self):
        return self.product_name

    # Return value
    def get_value(self):
        return self.value

    # Change the prodcut_name to new_name
    def change_name(self, new_name):
        if 0 < len(new_name) < 31:
            self.product_name = new_name
            self.save()
        else:
            print("Did not change the product name, new_name is invalid.", file=sys.stderr)

    # Change the value to new_val
    def change_value(self, new_val):
        if new_val > 0:
            self.value = new_val
            self.save()
        else:
            print("Value must be strictly postive. Did not change.", file=sys.stderr)


# LineItem class
class LineItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_date = models.DateTimeField('date added')

    def __str__(self):
        try:
            return str(self.product.product_name) + ': $' + str(self.total()) + ' (' + str(self.quantity) \
                   + '*$' + str(self.product.value) + ')'
        except ValueError:
            return "Line Item " + str(self.id)

    # Returns quantity
    def get_quantity(self):
        return self.quantity

    # Change the quantity to new_quantity, delete if new quantity is 0
    def change_quantity(self, new_quantity):
        if new_quantity > 0:
            self.quantity = new_quantity
            self.save()
        elif new_quantity == 0:
            self.delete()
        else:
            print("Cannot have a negative quantity.", file=sys.stderr)

    # Returns the total of the line item (quantity * value of product)
    def total(self):
        try:
            return self.quantity * self.product.value
        except ValueError:
            return 0


# Order class
class Order(models.Model):
    order_num = models.CharField(default=order_number(), max_length=16)
    added_date = models.DateTimeField('date added')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    lineitems = models.ManyToManyField(LineItem)

    def __str__(self):
        return self.order_num + ': $' + str(self.total())

    # Returns a queryset of the line items in product
    def get_items(self):
        return self.lineitems.all()

    # Creates and adds a line item corresponding to product name and quantity
    def create_item(self, product_name, quantity=1):
        try:
            product = Product.objects.get(product_name=product_name)
            item = product.lineitems.create(quantity=quantity, added_date=timezone.now())
            self.lineitems_set.add(item)
            return item
        except ObjectDoesNotExist:
            print("%s is not a product.\nPlease try again.", product_name, file=sys.stderr)

    # Adds an existing line item to order
    def add_item(self, product_name, lineitem):
        try:
            product = Product.objects.get(product_name=product_name)
            lineitem.save()
            product.lineitems_set.add(lineitem)
            self.lineitems_set.add(lineitem)
        except ObjectDoesNotExist:
            print("%s is not a product.\nPlease try again.", product_name, file=sys.stderr)

    # Returns the total of all line items in order
    def total(self):
        total = 0
        for item in self.lineitems.all():
            total += item.total()
        return total
