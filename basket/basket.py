from decimal import Decimal

from django.conf import settings

from store.models import Product

BASKET_SESSION_KEY = settings.BASKET_SESSION_KEY


class Basket():
    """
    A base Basket class, providing some default behaviors
    """

    def __init__(self, request):
        self.session = request.session
        
        if BASKET_SESSION_KEY not in request.session:
            basket = self.session[BASKET_SESSION_KEY] = {}
            # self.session['basket_qty'] = 0
            # self.session['basket_price'] = 0
        else:
            basket = self.session[BASKET_SESSION_KEY]

        self.basket = basket

    
    def add(self, product, product_qty):
        """
        Add item to basket session
        """

        product_id = str(product.pk)
        product_total_price = product.price * product_qty

        if product_id not in self.basket:
            # add new item to basket (item not in basket)
            self.basket[product_id] = {
                'id': int(product_id),
                'price': str(product.price),
                'qty': int(product_qty),
                'total_price': str(product_total_price),
                'title': product.title,
                'product_detail_url': product.get_api_url,
            }
        else:
            # add item to basket (item already in basket)
            total_price = Decimal(self.basket[product_id]['total_price'])
            total_price += product_total_price

            self.basket[product_id]['total_price'] = str(total_price)
            self.basket[product_id]['qty'] += product_qty

        self.save()

    
    def update(self, product, product_qty):
        product_id = str(product.pk)
        product_total_price = product.price * product_qty

        self.basket[product_id]['total_price'] = str(product_total_price)
        self.basket[product_id]['qty'] = product_qty

        self.save()
    

    def delete(self, product):
        """
        Delete item from basket session data
        """

        product_id = str(product.id)
        if product_id in self.basket:
            item = self.basket[product_id]
           
            # self.session['basket_qty'] -= item['qty']
            # self.session['basket_price'] -= float(item['total_price'])

            del self.basket[product_id]

        self.save()


    def save(self):
        """
        Save changes to basket session
        """

        self.session.modified = True


    def clear(self):
        """
        Remove basket from session (occurs when order and payment is completed)
        """
        del self.session[BASKET_SESSION_KEY]
        self.save()


    def __iter__(self):
        """
        Collect the product_id in the session data to query the db and return the products detail
        """
        product_ids = self.basket.keys()
        products_in_basket = Product.active_products.filter(pk__in=product_ids) 
        
        # copy the session data in to a new dict to save up memory for the session data
        basket = self.basket.copy()

        for product in products_in_basket:
            basket[str(product.id)]['product'] = product

        for item in basket.values():
            yield item
        
    @property
    def get_basket_price(self):
        """
        Get the basket total price
        """
        # return format(self.session['basket_price'], '.2f')
        return sum(Decimal(item['total_price']) for item in self.basket.values())
        

    @property
    def get_basket_qty(self):
        """
        Get the basket data and count the total qty
        """
        # return self.session['basket_qty']
        return sum(item['qty'] for item in self.basket.values())

