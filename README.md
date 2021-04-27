# E-Commerce

E-Commerce is my personal project demo, which consists of 2 parts:
* [Website](#websites) (using [Django](https://docs.djangoproject.com/en/3.2/) framework)
* [REST API](#rest-api) (using [Django Rest Framework](https://www.django-rest-framework.org/))

[Online demo](https://fns-ecommerce.herokuapp.com/)<br>

# Table of contents
* [Introduction](#introduction)
* [Websites](#websites)
* [REST API](#rest-api)
* [File Contents](#file-contents)

# Introduction

The websites part consists of different views, where either anonymous or authenticated user can search,visualize products, adding products to basket, paying and creating account to keep track of different orders.

The REST API part is a UI less utilizing [Django Rest Framework](https://www.django-rest-framework.org/) (DRF), containing distinct endpoints of corresponding models (Product, Category, basket session). 

<br>

# Websites

The picture below displayes the database schema of all models and partial fields used in this projects. The notations '1' means one and '*' means many, displaying the relationship between models. 

For example, the arrow pointing from 'users' to 'products is 1 to *, stating that the relationship betweem 'users' and 'products' is one-to-many relationship  

<br>

![image](https://user-images.githubusercontent.com/27566386/116015748-1f1dd300-a643-11eb-830f-1c0c1ee03fb1.png)

Features:
* Displaying all products
* Displaying single products
* Search for products
* Add or remove basket from basket
* Payment
* Keep record of orders (complete payment)
* Create account / login

## Payment
For the information of card payment, you can use any [test-authorized card number](https://stripe.com/docs/testing#cards), provided by [Stripe](https://stripe.com/docs) or you can use one below.

Card number: 4242424242424242 <br>
The date expiration of the card has to be a date in the future.

![image](https://user-images.githubusercontent.com/27566386/116315726-97a6a000-a7b9-11eb-8c9c-f642eac4d45b.png)

<br>

# REST API

There are 2 ways to test and visualize the REST API. The first view is to visualize directly via the URL, which is based on [DRF generic views](https://www.django-rest-framework.org/api-guide/generic-views/), as shown in the pictures below.

<br>

![image](https://user-images.githubusercontent.com/27566386/116017772-365fbf00-a649-11eb-9361-0e96e339e053.png)

<br>

The second one is to copy the URL and test via Postman.

<br>

## PERMISSIONS:

Some endpoints require authenticated user and admin permission, you may need authorization using the information below.

``Email: admin@gmail.com`` <br>
``Password: admin12345``

With the first view (DRF generic views), you can easily login at the home page. <br>
With Postman, you need to provide authorization, displayed below


![image](https://user-images.githubusercontent.com/27566386/116018501-ceaa7380-a64a-11eb-8a6d-505123e4babf.png)

<br>

## ENDPOINTS:

## Product List: [``/api/product/``](https://fns-ecommerce.herokuapp.com/api/product/)
* Methods: GET
* Permissions: [IsAuthenticated](https://www.django-rest-framework.org/api-guide/permissions/#isauthenticated)
* Description: displaying list of products 

<br>

## Category List: [``/api/category/``](https://fns-ecommerce.herokuapp.com/api/category/)
* Methods: GET
* Permissions: [IsAuthenticated](https://www.django-rest-framework.org/api-guide/permissions/#isauthenticated)
* Description: displaying list of categories

<br>

## Searching products by name and product code: 
* product_code: exact match
* product_title: starts-with

``/api/product/?search=<product_code>`` 
<br>

``/api/product/?search=<product_title>``

## Ordering search result by name and product code
i.e.

``/api/product/?search=<product_code>&ordering=title`` -> search products by 'product_code' and order search results by 'title' in ascending order.
<br>

``/api/product/?search=<product_title>&ordering=-product_code``

<br>

## Product Detail: ``/api/product/detail/<slug:slug>/``
* Methods: GET, PUT, DELETE
* Permissions: [IsAdminUser](https://www.django-rest-framework.org/api-guide/permissions/#isadminuser)
* Description: displaying detail/modify/delete single product

<br>

## Product Create: [``/api/product/create/``](https://fns-ecommerce.herokuapp.com/api/product/create/)
* Methods: POST
* Permissions: [IsAdminUser](https://www.django-rest-framework.org/api-guide/permissions/#isadminuser)
* Description: create new product
* Response body: {<br>
    "title": str, <br>
    "product_code": str,<br>
    "category": str,<br>
    "product_creator": str,<br>
    "price": float,<br>
    "image": file - optional<br>
}

<br>

## Shopping cart display: [``/api/basket/``](https://fns-ecommerce.herokuapp.com/api/basket/)
* Methods: GET
* Permissions: [AllowAny](https://www.django-rest-framework.org/api-guide/permissions/#allowany)
* Description: displaying all items in the shopping cart

<br>

## Shopping cart add: [``/api/basket/add/``](https://fns-ecommerce.herokuapp.com/api/basket/add/)
* Methods: POST
* Permissions: [AllowAny](https://www.django-rest-framework.org/api-guide/permissions/#allowany)
* Description: add item to shopping cart
* Request body: {<br>
    "product_id": int, <br>
    "qty": int<br>
}

<br>

## Shopping cart remove: [``/api/basket/remove/``](https://fns-ecommerce.herokuapp.com/api/basket/remove/)
* Methods: POST
* Permissions: [AllowAny](https://www.django-rest-framework.org/api-guide/permissions/#allowany)
* Request body: {<br>
    "product_id": int, <br>
}

<br>

## Shopping cart update: [``/api/basket/update/``](https://fns-ecommerce.herokuapp.com/api/basket/update/)
* Methods: PUT
* Permissions: [AllowAny](https://www.django-rest-framework.org/api-guide/permissions/#allowany)
* Request body: {<br>
    "product_id": int, <br>
    "qty": int<br>
}

<br>

# File Contents

The file contents consists of 7 apps:
* [core](https://github.com/nhat-tran-230297/eCommerce/tree/main/core): main app that handles settings and configuration
* [account](https://github.com/nhat-tran-230297/eCommerce/tree/main/account): 
    * models: User 
    * views: login, create account, activate account
* [store](https://github.com/nhat-tran-230297/eCommerce/tree/main/store): 
    * models: Product, Category 
    * views: home view, product list, product detail, search for products
* [basket](https://github.com/nhat-tran-230297/eCommerce/tree/main/basket): 
    * views: create basket session that stores product items, quantity and total price
* [payment](https://github.com/nhat-tran-230297/eCommerce/tree/main/payment):  
    * views: connect with Stripe, collect input date from payment form, create order and send email 
* [order](https://github.com/nhat-tran-230297/eCommerce/tree/main/order): 
    * models: Order, OrderItem 
    * views: when payment completes, create orders (including items from basket)
* [api](https://github.com/nhat-tran-230297/eCommerce/tree/main/api)
    * create REST API using Django Rest Framework
    * views: 
        * Search and list
            * Allow searching products by name and product code
            * Allow ordering search result by name and product code
        * View details of a product
            * Show product details from a single endpoint
        * Shopping cart
            * A product can be added to a cart and removed from it
        * Product management
            * Allow creating, modifying and deleting product


```
📦core
 ┣ 📂settings
 ┃ ┣ 📜base.py
 ┃ ┣ 📜development.py
 ┃ ┗ 📜__init__.py
 ┣ 📜asgi.py
 ┣ 📜db.sqlite3
 ┣ 📜urls.py
 ┣ 📜wsgi.py
 ┗ 📜__init__.py
📦account
 ┣ 📂migrations
 ┃ ┗ 📜__init__.py
 ┣ 📂tests
 ┃ ┣ 📜test_models.py
 ┃ ┣ 📜test_views.py
 ┃ ┗ 📜__init__.py
 ┣ 📜admin.py
 ┣ 📜apps.py
 ┣ 📜forms.py
 ┣ 📜models.py
 ┣ 📜tokens.py
 ┣ 📜urls.py
 ┣ 📜utils.py
 ┣ 📜views.py
 ┗ 📜__init__.py
📦api
 ┣ 📂migrations
 ┃ ┗ 📜__init__.py
 ┣ 📜admin.py
 ┣ 📜apps.py
 ┣ 📜serializers.py
 ┣ 📜tests.py
 ┣ 📜urls.py
 ┣ 📜views.py
 ┗ 📜__init__.py
 📦store
 ┣ 📂migrations
 ┃ ┗ 📜__init__.py
 ┣ 📂tests
 ┃ ┣ 📜test_models.py
 ┃ ┣ 📜test_views.py
 ┃ ┗ 📜__init__.py
 ┣ 📜admin.py
 ┣ 📜apps.py
 ┣ 📜context_processors.py
 ┣ 📜models.py
 ┣ 📜urls.py
 ┣ 📜views.py
 ┗ 📜__init__.py
📦basket
 ┣ 📂migrations
 ┃ ┗ 📜__init__.py
 ┣ 📂tests
 ┃ ┣ 📜test_views.py
 ┃ ┗ 📜__init__.py
 ┣ 📜apps.py
 ┣ 📜basket.py
 ┣ 📜context_processors.py
 ┣ 📜models.py
 ┣ 📜urls.py
 ┣ 📜views.py
 ┗ 📜__init__.py
 📦order
 ┣ 📂migrations
 ┃ ┗ 📜__init__.py
 ┣ 📜admin.py
 ┣ 📜apps.py
 ┣ 📜models.py
 ┣ 📜tests.py
 ┣ 📜urls.py
 ┣ 📜views.py
 ┗ 📜__init__.py
 📦payment
 ┣ 📂migrations
 ┃ ┗ 📜__init__.py
 ┣ 📜admin.py
 ┣ 📜apps.py
 ┣ 📜models.py
 ┣ 📜tests.py
 ┣ 📜urls.py
 ┣ 📜utils.py
 ┣ 📜views.py
 ┗ 📜__init__.py
📦templates
 ┣ 📂account
 ┃ ┣ 📂password
 ┃ ┃ ┣ 📜password_reset_complete.html
 ┃ ┃ ┣ 📜password_reset_confirm.html
 ┃ ┃ ┣ 📜password_reset_done.html
 ┃ ┃ ┣ 📜password_reset_email.html
 ┃ ┃ ┗ 📜password_reset_form.html
 ┃ ┣ 📂registration
 ┃ ┃ ┣ 📜account_activation_complete.html
 ┃ ┃ ┣ 📜account_activation_email.html
 ┃ ┃ ┣ 📜account_activation_invalid.html
 ┃ ┃ ┣ 📜login.html
 ┃ ┃ ┗ 📜register.html
 ┃ ┣ 📂user
 ┃ ┃ ┣ 📜dashboard.html
 ┃ ┃ ┣ 📜delete_confirm.html
 ┃ ┃ ┗ 📜edit.html
 ┃ ┗ 📜account_base.html
 ┣ 📂basket
 ┃ ┗ 📜summary.html
 ┣ 📂payment
 ┃ ┣ 📜payment_base.html
 ┃ ┣ 📜payment_complete.html
 ┃ ┗ 📜payment_form.html
 ┣ 📂store
 ┃ ┣ 📂category
 ┃ ┃ ┗ 📜category_product_list.html
 ┃ ┣ 📂product
 ┃ ┃ ┣ 📜product_detail.html
 ┃ ┃ ┗ 📜product_search_results.html
 ┃ ┗ 📜home.html
 ┣ 📜base.html
 ┗ 📜error.html
 📦media
 ┗ 📂images
 ┃ ┣ 📜default.png
📦static
 ┣ 📂account
 ┃ ┗ 📂css
 ┃ ┃ ┗ 📜account.css
 ┣ 📂basket
 ┃ ┣ 📂css
 ┃ ┃ ┗ 📜basket.css
 ┃ ┗ 📂js
 ┃ ┃ ┣ 📜basket_update_basket_summary_view.js
 ┃ ┃ ┗ 📜basket_update_product_detail_view.js
 ┣ 📂core
 ┃ ┗ 📂css
 ┃ ┃ ┗ 📜base.css
 ┣ 📂payment
 ┃ ┗ 📂js
 ┃ ┃ ┗ 📜payment_form.js
 ┗ 📂store
 ┃ ┣ 📂css
 ┃ ┗ 📂js
 📜manage.py