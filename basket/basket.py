from decimal import Decimal

from store.models import Product


class Basket():
    """
    A base Basket class, providing some default behaviors
    """

    def __init__(self, request):
        self.session = request.session
        
        if 'basket' not in request.session:
            basket = self.session['basket'] = {}
            self.session['basket_quantity'] = 0
            self.session['basket_price'] = 0
        else:
            basket = self.session['basket']

        self.basket = basket

    
    def add(self, product, product_quantity):
        """
        Add and update user's basket session data
        """

        product_id = str(product.id)
        product_price = product.price * product_quantity

        if product_id not in self.basket:
            # add new basket info to session data
            self.basket[product_id] = {
                'total_price': str(product_price),
                'quantity': int(product_quantity)
            }
        else:
            # update session basket data
            total_price = Decimal(self.basket[product_id]['total_price'])
            total_price += product_price

            self.basket[product_id]['total_price'] = str(total_price)
            self.basket[product_id]['quantity'] += product_quantity

        self.session['basket_quantity'] += product_quantity
        self.session['basket_price'] += float(product_price)

        self.save()
    

    def delete(self, product):
        """
        Delete item from basket session data
        """

        product_id = str(product.id)
        if product_id in self.basket:
            item = self.basket[product_id]
           
            self.session['basket_quantity'] -= item['quantity']
            self.session['basket_price'] -= float(item['total_price'])

            del self.basket[product_id]

        self.save()


    def save(self):
        self.session.modified = True

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
        return format(self.session['basket_price'], '.2f')
        

    @property
    def get_basket_quantity(self):
        """
        Get the basket data and count the total quantity
        """
        return self.session['basket_quantity']

