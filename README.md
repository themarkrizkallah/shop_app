# shop app

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for testing purposes.

### Prerequisites

You need to have [Python](https://www.python.org/downloads/) and [Django](https://docs.djangoproject.com/en/2.1/topics/install/) installed.

## Running the server
```
$ cd mark-dev-challenge
$ python3 manage.py runserver
```

Then open [http://localhost:8000/](http://localhost:8000/) in your browser.

Voila, you can now play around with the api!

[http://localhost:8000/](http://localhost:8000/) or [http://localhost:8000/shops](http://localhost:8000/shops) presents you with a list of all the *shops* (`Shop` objects) currently available.

**Note**: You can create an alias to `python3` by running
```
$ alias python=python3
```

I found this easier than typing `python3` everytime!

## How to Use

### Accessing the API
Once the server is running and you are on [http://localhost:8000/](http://localhost:8000/), you have 3 to access the api:

1. Access the api in a python shell
    1. Open a shell
        ```
        $ python3 manage.py shell
        ```
    2. Import the appropriate objects
        ```p
        >> from shops.models import Shop, Product, Order, LineItem
        ```
    3. You can now access the api
2. Visit [http://localhost:8000/admin](http://localhost:8000/admin)
    - Log in using the following credentials:
        - **username**: *shopify*
        - **password**: *markrizkallah*
    - You can now create, retrieve, update, and delete objects

3. Visit [http://localhost:8000/shops](http://localhost:8000/shops) to view what's currently listed on the platform
    -  Every `Shop` can have orders (`Order` objects) and products (`Product` objects).
    -  In order to see the contents of the shop:
        1. First, click on the appropriate shop name
        2. Then, click on either *Products* or *Orders*

Regardless of your choice, you will be able to create, read, update, and delete (*CRUD*) `Shop`, `Product`, `Order`, and `LineItem` objects.

Since using the *admin* panel is fairly straight forward, I will mainly outline how to use the api in a *python shell*. But first, we'll outlay our objects.

### Objects
Our platform has 4 main objects:
1. `Shop` has:
    - A unique name 
    - Many `Product` and many `Order` objects
2. `Product` has:
    - A unique name
    - A value (its price)
    - Many `LineItem` objects
3. `Order` has:
    - A unique, randomly generated 16 digit order number 
    - Has many `LineItem` objects
4. `LineItem` has:
    - A quantity (# of the `Product` it represents)

We'll now examine the objects one by one.

**Note**: You MUST have the objects imported for the following to work. To do so, your shell/.py file must have

`from shops.models import Shop, Product, Order, LineItem`


#### Shop
A quick summary of how to interact with `Shop` objects:
```python
from shops.models import Shop, Product, Order

# Returns a QuerySet (iterable) of all the Shops
Shop.get_shops()

# Create and return a new Shop
# Note: names of all objects (not just Shops) must be <= 30 chars
Shop.create('Shop #1')

# Returns a Shop with the name 'name'
Shop.get('shop-name')

# We now need an instance of Shop for the following to work
shop1 = Shop.get('Shop #1')

# Change the name of shop1
shop1.change_name('new-name')

# Returns a QuerySet of all Products in a Shop
shop1.get_products()

# Returns a QuerySet of all Orders in a Shop
shop1.get_orders()

# Creates and returns a Product in a Shop
# Note: For creation to work, shop must be an actual shop
#       i.e. must have used Shop.create('Shop #1') previously
shop1.create_product('product-name')

# Creates and returns an Order in a Shop
# Note: For creation to work, shop must be an actual shop
shop1.create_order()

# Returns a Product with a specific name
shop1.get_product('product-name')

# Returns an Order with a specific number
shop1.get_order('1537-730818-8025')

# Delete shop1
# Note: Deletes Shop, and all Products, Orders, and LineItems in it
shop1.delete()
```

#### Product
A quick summary of how to interact with `Product` objects:
```python
from shops.models import Shop, Product

shop1 = Shop.get('Shop #1')

# We create a product in shop1
# Note: value must be strictly positive
shop.create_product('Product #0', 5)

# We get "Product #1"
prod1 = shop.get_product('Product #0')

# Returns the Product name
prod1.get_name()

# Returns the Product value
prod1.get_value()

# Rename prod1
prod1.change_name('Product #1')

# Change value of prod1
prod1.change_value(10)

# Delete prod1
# Note: Deletes all LineItems associated with Product as well
prod1.delete()
```

#### Order and LineItem
A quick summary of how to interact with `Order` and `LineItem` objects:
```python
from shops.models import Shop, Product, Order, LineItem

shop1 = Shop.get('Shop #1')

# Creates an Order with a randomly generated order number
order1 = shop1.create_order()

# Creates a LineItem in order1 that refers to 'Product #1' and has quantity 2
item1 = order1.create_item('Product #1', 2)

# Changes quantity of item1 to 1
# Note: If new_quantity is 0, item1 is deleted from order1
item1.change_quantity(1)

# Returns the value of a LineItem (product value * quantity)
item1.total()

# Returns a QuerySet of all LineItems in order1
order1.get_items()

# Returns the sum of all the LineItems in order1
order1.total()

# Delete item1
item1.delete()

# Delete order1
order1.delete()
```

## Database
I have a *PostgreSQL* database instance on *Amazon RDS*. I populated the database with values for you to test; however, feel free to add your own either through the *admin* dashboard or through a *shell*.

If you need direct access to the database, check [shopify_dev/settings.py](shop_app/settings.py) for information.

## Deployment
I deployed the web API to *Google Kubernetes Engine (GKE)*.
I have attached the [shops.yaml](shops.yaml) and [Dockerfile](Dockerfile). The pods are running and are not logging any errors.

```
$ kubectl get pods

NAME                     READY     STATUS    RESTARTS   AGE
shops-66567974bd-b4jww   1/1       Running   6          2h
shops-66567974bd-v6tzt   1/1       Running   6          2h
shops-66567974bd-v92x6   1/1       Running   6          2h
```

That being said, entering the [http://35.188.150.137/](http://35.188.150.137/) in the browser does not work.


**Example** of what happens when I try to connect via the terminal:
```
$ kubectl get services shops

NAME      TYPE           CLUSTER-IP      EXTERNAL-IP      PORT(S)        AGE
shops     LoadBalancer   10.55.242.133   35.188.150.137   80:31830/TCP   2h

$ curl 35.188.150.137
curl: (7) Failed to connect to 35.188.150.137 port 80: Connection refused
```

## Built With

* [Django](https://www.djangoproject.com/) - Powered the server-side web api
* [PostgreSQL](https://www.postgresql.org/) - Database system
* [AWS](https://aws.amazon.com/) - Amazon RDS used to host the database instance
